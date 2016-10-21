import re
import pytest
import string
import random

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


@pytest.fixture(scope="module")
def fusor_admin_username(variables):
    return variables['credentials']['fusor']['username']


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


def test_create_deployment(osp_api, deployment_id):
    deployment_name = 'pytest-{}-osp-cfme'.format(deployment_id)
    deployment_desc = 'pytest for OSP API deployment'

    assert osp_api.create_deployment(deployment_name, deployment_desc)


def test_list_deployment(osp_api):
    assert osp_api.list_deployments()


def test_delete_deployment(osp_api, deployment_id):
    assert osp_api.delete_deployment()


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


def test_osp_api(osp_api, variables):
    dep = variables['deployment']
    dep_osp = dep['products']['osp']
    dep_cfme = dep['products']['cfme']
    dep_ose = dep['products']['ose']
    dep_sat = dep['products']['sat']
    masktocidr = {"255.255.255.0": "/24", "255.255.0.0": "/16", "255.0.0.0": "/8", }

    deploy_cfme = 'cfme' in dep['install']
    deploy_ose = 'ocp' in dep['install']
    deployment_name = 'pytest-{}-osp{}{}'.format(
        dep['deployment_id'], '-cfme' if deploy_cfme else '', '-ocp' if deploy_ose else '')
    deployment_desc = 'Pytest of the fusor api for deploying OSP'
    undercloud_ip = dep_osp['undercloud_address']
    undercloud_user = dep_osp['undercloud_user']
    undercloud_pass = dep_osp['undercloud_pass']
    overcloud_nodes = dep_osp['overcloud_nodes']
    overcloud_controller_count = dep_osp['controller_count']
    overcloud_compute_count = dep_osp['controller_count']
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
    rhn_sma_uuid = get_sma_uuid(osp_api, rhn_username, rhn_password, dep_sat['rhsm_satellite_name'])
    ose_sub_pool_name = dep_ose['subscription']['name']
    ose_sub_quantity = dep_ose['subscription']['quantity']
    osp_deploy_ramdisk_name = 'bm-deploy-ramdisk'
    osp_deploy_kernel_name = 'bm-deploy-kernel'

    assert osp_api.create_deployment(deployment_name, deployment_desc,
                                     deploy_cfme=deploy_cfme, deploy_ose=deploy_ose)

    osp_api.refresh_deployment_info()
    assert osp_api.add_undercloud(undercloud_ip, undercloud_user, undercloud_pass)
    osp_api.refresh_deployment_info()

    osp_images = osp_api.get_openstack_images()
    assert osp_images  # "Unable to get the openstack image info"

    ramdisk_image = next(
        image for image in osp_images['images'] if (image['name'] == osp_deploy_ramdisk_name))
    kernel_image = next(
        image for image in osp_images['images'] if (image['name'] == osp_deploy_kernel_name))

    assert kernel_image  # "Unable to get the openstack kernel image info"
    assert ramdisk_image  # "Unable to get the openstack ramdisk image info"

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
