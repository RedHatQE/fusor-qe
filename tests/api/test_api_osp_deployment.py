import re
import pytest
import string
import random
from time import sleep

from lib.api import fusor_api


def parse_ip_from_url(url):
    """
    Use a regular expression to parse the IP from a url.
    Will return IP address if not protocol is specified
    This assumes that the url does not use a DNS address
    """
    # Regex groups 1 and 2 will make up the protocol and separator
    # Group 3 will be the IP address
    # Group for will be everything after the IP
    url_pattern = r'((https?)://)?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(.*)'
    re_sult = re.match(url_pattern, url)

    protocol, proto_full, ip, url_tail = re_sult.groups()

    return ip


# TODO: Make this global for all QCI tests
@pytest.fixture(scope="module")
def deployment_name(request):
    dep_name = request.config.getoption("--deployment-name")
    print "Deployment name to test: {}".format(dep_name)
    return dep_name


# TODO: Make this global for all QCI tests
@pytest.fixture(scope="module")
def fusor_admin_username(variables):
    return variables['credentials']['fusor']['username']


# TODO: Make this global for all QCI tests
@pytest.fixture(scope="module")
def fusor_admin_password(variables):
    return variables['credentials']['fusor']['password']


@pytest.fixture(scope="module")
def deployment_id(variables):
    """
    Retrieve deployment id used throughout this test
    Currently just generates a random string
    """
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])


@pytest.fixture(scope="module")
def osp_api(fusor_admin_username, fusor_admin_password, base_url):
    """
    OSPFusorApi object with methods for accessing/editing OSP deployment objects
    """
    fusor_ip = parse_ip_from_url(base_url)
    return fusor_api.OSPFusorApi(fusor_ip, fusor_admin_username, fusor_admin_password)


def deployment_attach_sub(
        osp_api, rhn_username, rhn_password, rhn_sma_uuid, sub_name, sub_quantity, **kwargs):
    """
    Attach the specified subscriptions to the deployment loaded in the osp_api object

    attach_subs must be a list of dictionaries with each item having the following keys
    {
      name - Name of the subscription
      pool_id - uuid of the pool to attach
      quantity - Quantity of subs needed for this deployment.
    }
    """

    osp_api.rhn_login(rhn_username, rhn_password)
    consumer = osp_api.rhn_get_consumer(rhn_sma_uuid)
    osp_api.rhn_set_upstream_consumer(consumer['name'], consumer['uuid'])
    subscriptions = osp_api.rhn_get_consumer_subscriptions(rhn_sma_uuid)

    # Each run we reset the default subscriptions (pool) to rhsm_pools in the yaml
    # Deployment products might need additional subs so loop through available
    #  subs and add attach as subscriptions needed
    # TODO: Compare quantity needed to quantity available
    for sub in subscriptions:
        pool = sub['pool']
        qty_attached = sub['quantity']
        pool_id = pool['id']
        pool_name = pool['productName']
        if pool_name == sub_name:
            if qty_attached < sub_quantity:
                qty_additional = sub_quantity - qty_attached
                osp_api.rhn_attach_subscription(
                    consumer['uuid'], pool_id, qty_additional)


def get_sma_uuid(osp_api, rhn_username, rhn_password, sma_name):
    osp_api.rhn_login(rhn_username, rhn_password)
    owner = osp_api.rhn_owner_info(rhn_username)
    consumers = osp_api.rhn_list_consumers(owner['key'])

    sma_uuid = None
    for consumer in consumers:
        if consumer['name'] == sma_name:
            sma_uuid = consumer['uuid']
            break

    return sma_uuid


def test_osp_api(osp_api, variables, deployment_name):
    dep = variables['deployment']
    dep_osp = dep['products']['osp']
    dep_cfme = dep['products']['cfme']
    dep_ose = dep['products']['ose']
    dep_sat = dep['products']['sat']
    masktocidr = {"255.255.255.0": "/24", "255.255.0.0": "/16", "255.0.0.0": "/8", }

    deploy_cfme = 'cfme' in dep['install']
    deploy_ose = 'ocp' in dep['install']
    if not deployment_name:
        deployment_name = 'pytest-osp-api-{}{}'.format(
            dep['deployment_id'], '-cfme' if deploy_cfme else '', '-ocp' if deploy_ose else '')
    deployment_desc = 'Pytest of the fusor api for deploying OSP'
    undercloud_ip = dep_osp['undercloud_address']
    undercloud_user = dep_osp['undercloud_user']
    undercloud_pass = dep_osp['undercloud_pass']
    overcloud_nodes = dep_osp['overcloud_nodes']
    overcloud_controller_count = dep_osp['controller_count']
    overcloud_compute_count = dep_osp['compute_count']
    cinder_role_count = dep_osp.get('cinder_count', 0)
    swift_role_count = dep_osp.get('swift_count', 0)
    ceph_role_count = dep_osp.get('ceph_count', 0)  # Ceph local storage not supported in QCI
    overcloud_admin_pass = dep_osp['undercloud_pass']  # Sync overcloud pw with undercloud
    overcloud_prov_network = '{}{}'.format(
        dep_osp['network']['provision_network']['network'],
        masktocidr[dep_osp['network']['provision_network']['subnet']])
    overcloud_pub_network = '{}{}'.format(
        dep_osp['network']['public_network']['network'],
        masktocidr[dep_osp['network']['public_network']['subnet']])
    overcloud_pub_gateway = dep_osp['network']['public_network']['gateway']
    cfme_root_password = dep_cfme['cfme_root_password']
    rhn_username = variables['credentials']['cdn']['username']
    rhn_password = variables['credentials']['cdn']['password']
    rhn_sma_uuid = dep_sat['rhsm_satellite']['uuid']
    ose_sub_pool_name = dep_ose['subscription']['name']
    ose_sub_quantity = dep_ose['subscription']['quantity']
    osp_deploy_ramdisk_name = 'bm-deploy-ramdisk'
    osp_deploy_kernel_name = 'bm-deploy-kernel'
    osp_images = None
    ramdisk_image = None
    kernel_image = None

    assert osp_api.create_deployment(deployment_name, deployment_desc,
                                     deploy_cfme=deploy_cfme, deploy_ose=deploy_ose)

    osp_api.refresh_deployment_info()
    assert osp_api.add_undercloud(undercloud_ip, undercloud_user, undercloud_pass)
    osp_api.refresh_deployment_info()

    image_query_wait = 10
    image_query_retries = 0
    image_query_retries_max = 3
    # Retry undercloud image query when automation moves faster than fusor
    while ((not osp_images or not kernel_image or not ramdisk_image) and
            image_query_retries < image_query_retries_max):
        osp_images = osp_api.get_openstack_images()
        image_query_retries += 1

        try:
            assert osp_images  # "Unable to get the openstack image info"

            ramdisk_iterator = (
                image for image in osp_images['images'] if (
                    image['name'] == osp_deploy_ramdisk_name))
            ramdisk_image = next(ramdisk_iterator, None)

            kernel_iterator = (
                image for image in osp_images['images'] if (
                    image['name'] == osp_deploy_kernel_name))
            kernel_image = next(kernel_iterator, None)

            assert kernel_image  # "Unable to get the openstack kernel image info"
            assert ramdisk_image  # "Unable to get the openstack ramdisk image info"
        except AssertionError:
            if image_query_retries >= image_query_retries_max:
                print 'Maximum retries ({}) for querying openstack images has been reached'.format(
                    image_query_retries)
                raise

            print 'Retrying openstack image query - ({})'.format(image_query_retries)
            osp_images = None
            ramdisk_image = None
            kernel_image = None
            sleep(image_query_wait)

    for node in overcloud_nodes:
        assert osp_api.register_nodes(
            node['driver_type'],
            node['host_ip'],
            node['host_username'],
            node['host_password'],
            node['mac_address'],
            kernel_image['id'],
            ramdisk_image['id'])
        # "Failed to register OSP node: {}".format(node['mac_address'])

    osp_api.refresh_deployment_info()
    assert osp_api.wait_for_node_registration()
    # 'Overcloud nodes failed to finish registration successfully'

    # TODO: Verify that the finished tasks didn't fail
    overcloud_node_count = len(overcloud_nodes)

    assert osp_api.set_overcloud_node_count(overcloud_node_count)
    # 'Unable to set the overcloud node count to {}'.format(overcloud_node_count)

    osp_api.node_flavors()
    # Since nodes have the same HW specs we only have 1 flavor
    flavor_name = osp_api.fusor_data['osp_flavors'][0]['name']

    assert osp_api.update_role_controller(flavor_name, overcloud_controller_count)
    # "Unable to update controller role and count"

    assert osp_api.update_role_compute(flavor_name, overcloud_compute_count)
    # "Unable to update compute role and count"

    # "Assigning cinder role flavor ({}) and count ({})".format( flavor_name, storage_role_count))
    assert osp_api.update_role_cinder(flavor_name, cinder_role_count)
    # "Unable to update cinder role and count"

    # "Assigning swift role flavor ({}) and count ({})".format(flavor_name, swift_role_count))
    assert osp_api.update_role_swift(flavor_name, swift_role_count)
    # "Unable to update swift role and count"

    # Local ceph storage not supported by QCI
    assert osp_api.update_role_ceph(flavor_name, ceph_role_count)
    # "Unable to update ceph role and count"

    # This should only be run for nested deployments. Baremetal doesn't need this
    assert osp_api.set_nova_libvirt_type()
    # "Unable to set the overcloud libvirt type to {}".format(overcloud_libvirt_type))

    # "Setting overcloud credentials")
    osp_api.set_creds_overcloud(overcloud_admin_pass)

    assert osp_api.set_overcloud_network(
        overcloud_prov_network,
        overcloud_pub_network,
        overcloud_pub_gateway)
    # "Unable to set the overcloud network info"

    if deploy_cfme:
        # "Setting info for a Cloudforms Deployment"
        # "Setting CFME passwords"
        assert osp_api.set_creds_cfme(cfme_root_password)
        # "Unable to set the CFME passwords")

    if deploy_ose:
        # "OpenShift automation isn't implemented yet")
        assert 0

    deployment_attach_sub(
        osp_api, rhn_username, rhn_password, rhn_sma_uuid, ose_sub_pool_name, ose_sub_quantity)

    # Sync with overcloud so we don't clobber any values that are set by fusor (overcloud admin pw)
    # "Syncing OpenStack data with fusor"
    osp_api.sync_openstack()

    # "Starting OpenStack deployment")

    assert osp_api.deploy()


# TODO: This should be generic for any type of deployment
def test_osp_api_deployment_success(osp_api, variables, deployment_name):
    """
    Query the fusor deployment object for the status of the Deploy task
    """
    if deployment_name:
        osp_api.load_deployment(deployment_name)

    dep = variables['deployment']

    deployment_time_max = dep.get('deployment_timeout', 240)
    deployment_success = False
    fail_message = "Deployment FAILED"
    # Wait a while for the deployment to complete (or fail),
    for minutes in range(deployment_time_max):
        sleep(60)
        progress = osp_api.get_deployment_progress()
        osp_api.refresh_deployment_info()

        if(progress['result'] == 'success' and
           progress['state'] == 'stopped' and
           progress['progress'] == 1.0):
            deployment_success = True
            print 'OpenStack Deployment Succeeded!'
            assert deployment_success
        elif progress['result'] == 'error' and progress['state'] == 'paused':
            deployment_success = False
            deployment_task_uuid = osp_api.fusor_data['deployment']['foreman_task_uuid']
            foreman_task = next(
                task for task in osp_api.fusor_data['foreman_tasks'] if(
                    task['id'] == deployment_task_uuid))

            # Loop through all sub tasks until we find one paused w/ error
            for sub_task in foreman_task['sub_tasks']:
                if sub_task['result'] == 'error':
                    sub_task_info = osp_api.foreman_task(sub_task['id'])['foreman_task']
                    fail_message = 'Deployment Failed: {} -> {}'.format(
                        sub_task_info['label'], sub_task_info['humanized_errors'])
                    assert deployment_success, fail_message

            # If we got here then the logic for finding the failed task needs to be fixed
            fail_message = "Unable to find the failed subtask for task: {}".format(
                '\n'.join([step['action_class'] for step in foreman_task['failed_steps']]))

            assert deployment_success, fail_message

    assert deployment_success, "DEFAULT: {}".format(fail_message)
