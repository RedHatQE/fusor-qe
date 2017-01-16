import pytest
import string
import random
from urlparse import urlsplit
from time import sleep

from lib.api import fusor_api


def parse_ip_from_url(url):
    """
    This will return the IP address from a valid url scheme.
    Since urlparse won't separate the port, if present, from the IP we have to do it manually
    """
    up = urlsplit(url)

    ip = up.netloc
    if up.port:
        ip, port = ip.split(':')

    return ip


# TODO: Make this global for all QCI tests
@pytest.fixture(scope="module")
def deployment_name(request):
    dep_name = request.config.getoption("--deployment-name")
    print "Deployment name to test: {}".format(dep_name)
    return dep_name


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
def dep_api(fusor_admin_username, fusor_admin_password, base_url):
    """
    RHEVFusorApi object with methods for accessing/editing RHEV deployment objects
    """
    fusor_ip = parse_ip_from_url(base_url)
    return fusor_api.QCIDeploymentApi(fusor_ip, fusor_admin_username, fusor_admin_password)


def deployment_attach_subscriptions(
        dep_api, rhn_username, rhn_password, rhn_sma_uuid, sub_name, sub_quantity, **kwargs):
    """
    Attach the specified subscriptions to the deployment loaded in the dep_api object

    attach_subs must be a list of dictionaries with each item having the following keys
    {
      name - Name of the subscription
      pool_id - uuid of the pool to attach
      quantity - Quantity of subs needed for this deployment.
    }
    """

    dep_api.rhn_login(rhn_username, rhn_password)
    consumer = dep_api.rhn_get_consumer(rhn_sma_uuid)
    dep_api.rhn_set_upstream_consumer(consumer['name'], consumer['uuid'])
    subscriptions = dep_api.rhn_get_consumer_subscriptions(rhn_sma_uuid)

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
                dep_api.rhn_attach_subscription(
                    consumer['uuid'], pool_id, qty_additional)


def test_api_deployment(dep_api, variables, deployment_name):
    dep = variables['deployment']
    dep_rhv = dep['products']['rhv']
    dep_osp = dep['products']['osp']
    dep_cfme = dep['products']['cfme']
    dep_ose = dep['products']['ose']
    dep_sat = dep['products']['sat']

    masktocidr = {"255.255.255.0": "/24", "255.255.0.0": "/16", "255.0.0.0": "/8", }

    enable_access_insights = dep_sat['enable_access_insights']
    rhv_is_self_hosted = 'selfhost' in dep_rhv['rhv_setup_type']
    rhevm_mac = dep_rhv['rhvm_mac'] if not rhv_is_self_hosted else None
    rhevh_macs = dep_rhv['rhvh_macs']
    data_address = dep_rhv['data_domain_address']
    data_name = dep_rhv['data_domain_name']
    data_path = dep_rhv['data_domain_share_path']
    export_address = dep_rhv['export_domain_address']
    export_name = dep_rhv['export_domain_name']
    export_path = dep_rhv['export_domain_share_path']
    selfhosted_name = dep_rhv['selfhosted_domain_name']
    selfhosted_address = dep_rhv['selfhosted_domain_address']
    selfhosted_path = dep_rhv['selfhosted_domain_share_path']
    selfhosted_engine_hostname = dep_rhv['self_hosted_engine_hostname'] or 'rhv-selfhosted-engine'
    deploy_rhv = 'rhv' in dep['install']
    deploy_osp = 'osp' in dep['install']
    deploy_cfme = 'cfme' in dep['install']
    deploy_ose = 'ocp' in dep['install']
    if not deployment_name:
        deployment_name = 'pytest-api{}{}{}{}'.format(
            dep['deployment_id'],
            '-rhv' if deploy_cfme else '',
            '-osp' if deploy_cfme else '',
            '-cfme' if deploy_cfme else '',
            '-ocp' if deploy_ose else '')
    deployment_desc = 'API deployment using pytest'

    rhev_admin_password = dep_rhv['rhvm_adminpass']
    cfme_root_password = dep_cfme['cfme_admin_password']
    cfme_install_loc = dep_cfme['cfme_install_loc']
    cfme_root_password = dep_cfme['cfme_root_password']

    ose_install_loc = dep_ose['install_loc']
    ose_number_master_nodes = dep_ose['number_master_nodes']
    ose_master_vcpu = dep_ose['master_vcpu']
    ose_master_ram = dep_ose['master_ram']
    ose_master_disk = dep_ose['master_disk']
    ose_number_worker_nodes = dep_ose['number_worker_nodes']
    ose_node_vcpu = dep_ose['node_vcpu']
    ose_node_ram = dep_ose['node_ram']
    ose_node_disk = dep_ose['node_disk']
    ose_storage_size = dep_ose['storage_size']
    ose_storage_name = dep_ose['storage_name']
    ose_storage_host = dep_ose['storage_host']
    ose_export_path = dep_ose['export_path']
    ose_username = dep_ose['username']
    ose_user_password = dep_ose['user_password']
    ose_subdomain_name = dep_ose['subdomain_name'] if dep_ose['subdomain_name'] else dep['deployment_id']
    ose_sample_app_name = 'openshift_sample_helloworld'
    ose_sample_apps = dep_ose['sample_apps']  # List of sample apps to include in the deployment
    ose_sub_pool_name = dep_ose['subscription']['name']
    ose_sub_quantity = dep_ose['subscription']['quantity']

    undercloud_ip = dep_osp['undercloud_address']
    undercloud_user = dep_osp['undercloud_user']
    undercloud_pass = dep_osp['undercloud_pass']
    overcloud_nodes = dep_osp['overcloud_nodes']
    osp_deploy_ramdisk_name = 'bm-deploy-ramdisk'
    osp_deploy_kernel_name = 'bm-deploy-kernel'
    osp_images = None
    ramdisk_image = None
    kernel_image = None
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
    overcloud_libvirt_type = 'qemu'
    rhn_username = variables['credentials']['cdn']['username']
    rhn_password = variables['credentials']['cdn']['password']
    rhn_sma_uuid = dep_sat['rhsm_satellite']['uuid']

    assert dep_api.create_deployment(
        deployment_name, deployment_desc,
        deploy_rhv=deploy_rhv,
        deploy_osp=deploy_osp,
        deploy_cfme=deploy_cfme, deploy_ose=deploy_ose,
        access_insights=enable_access_insights), \
        "Unable to create RHEV deployment ({})".format(deployment_name)

    if deploy_rhv:
        assert dep_api.set_rhv_hosts(rhevh_macs, rhevm_mac), "Unable to set the RHEV Hosts"

        if rhv_is_self_hosted:
            dep_api.set_deployment_property('rhev_self_hosted_engine_hostname', selfhosted_engine_hostname)

        # log.info("Setting the RHEV credentials")
        assert dep_api.set_creds_rhv(rhev_admin_password), "Unable to set RHEV credentials"

        # log.info("Setting NFS storage values")
        assert dep_api.set_nfs_storage_rhv(
            data_name, data_address, data_path,
            export_name, export_address, export_path,
            selfhosted_name, selfhosted_address, selfhosted_path), \
            "Unable to set the NFS storage for the deployment"

    if deploy_cfme:
        assert dep_api.set_install_location_cfme(cfme_install_loc), \
            "Unable to set the CFME install location"
        assert dep_api.set_creds_cfme(cfme_root_password), \
            "Unable to set the CFME root/admin passwords"

    if deploy_ose:
        assert dep_api.set_install_location_ocp(ose_install_loc), \
            "Unable to set the OpenShift install location"

        assert dep_api.ose_set_master_node_specs(
            ose_number_master_nodes,
            ose_master_vcpu,
            ose_master_ram,
            ose_master_disk), 'Unable to set the OpenShift master node specs'

        assert dep_api.ose_set_worker_node_specs(
            ose_number_worker_nodes,
            ose_node_vcpu,
            ose_node_ram,
            ose_node_disk), 'Unable to set the OpenShift worker node specs'

        assert dep_api.ose_set_storage_size(ose_storage_size), \
            'Unable to set the OpenShift storage size for docker to {}'.format(
                ose_storage_size)

        assert dep_api.set_ose_nfs_storage(
            ose_storage_name,
            ose_storage_host,
            ose_export_path), 'Unable to set the OpenShift NFS storage'

        assert dep_api.set_ose_creds(ose_username, ose_user_password), \
            'Unable to set the OpenShift credentials'

        assert dep_api.set_ose_subdomain(ose_subdomain_name), \
            'Unable to set the OpenShift subdomain name'

        if ose_sample_apps:
            for app in ose_sample_apps:
                # Do some translation since the yaml app name value defaults to the element id
                if 'hello_world' in app:
                    assert dep_api.set_deployment_property(ose_sample_app_name, True), \
                        'Unable to enable OpenShift sample application hello_world'

    if deploy_osp:
        dep_api.refresh_deployment_info()
        assert dep_api.add_undercloud(undercloud_ip, undercloud_user, undercloud_pass)
        dep_api.refresh_deployment_info()

        image_query_wait = 10
        image_query_retries = 0
        image_query_retries_max = 3
        # Retry undercloud image query when automation moves faster than fusor
        while ((not osp_images or not kernel_image or not ramdisk_image) and
                image_query_retries < image_query_retries_max):
            osp_images = dep_api.get_openstack_images()
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
                    print 'Maximum retries ({}) for querying osp images has been reached'.format(
                        image_query_retries)
                    print "Image Info:\n", osp_images
                    raise

                print 'Retrying openstack image query - ({})'.format(image_query_retries)
                osp_images = None
                ramdisk_image = None
                kernel_image = None
                sleep(image_query_wait)

        for node in overcloud_nodes:
            assert dep_api.register_osp_nodes(
                node['driver_type'],
                node['host_ip'],
                node['host_username'],
                node['host_password'],
                node['mac_address'],
                kernel_image['id'],
                ramdisk_image['id']), \
                "Failed to register node for introspection: {}".format(node['mac_address'])

        dep_api.refresh_deployment_info()
        assert dep_api.wait_for_osp_node_registration(), \
            'Overcloud nodes failed to finish registration successfully'

        # TODO: Verify that the finished tasks didn't fail
        overcloud_node_count = len(overcloud_nodes)

        assert dep_api.set_overcloud_node_count(overcloud_node_count), \
            'Unable to set the overcloud node count to {}'.format(overcloud_node_count)

        dep_api.get_osp_node_flavors()
        # Since nodes have the same HW specs we only have 1 flavor
        flavor_name = dep_api.fusor_data['osp_flavors'][0]['name']

        assert dep_api.update_osp_role_controller(flavor_name, overcloud_controller_count), \
            "Unable to update controller role and count({})".format(
                flavor_name, overcloud_controller_count)

        assert dep_api.update_osp_role_compute(flavor_name, overcloud_compute_count), \
            "Unable to update compute role and count({})".format(
                flavor_name, overcloud_compute_count)

        assert dep_api.update_osp_role_cinder(flavor_name, cinder_role_count), \
            "Unable to update block storage role and count({})".format(
                flavor_name, cinder_role_count)

        assert dep_api.update_osp_role_swift(flavor_name, swift_role_count), \
            "Unable to update object role and count({})".format(
                flavor_name, swift_role_count)

        assert dep_api.update_osp_role_ceph(flavor_name, ceph_role_count)

        # This should only be run for nested deployments. Baremetal doesn't need this
        assert dep_api.set_nova_libvirt_type(overcloud_libvirt_type), \
            "Unable to set the overcloud libvirt type to {}".format(overcloud_libvirt_type)

        # "Setting overcloud credentials")
        dep_api.set_creds_overcloud(overcloud_admin_pass)

        assert dep_api.set_overcloud_network(
            overcloud_prov_network,
            overcloud_pub_network,
            overcloud_pub_gateway), \
            "Unable to set the overcloud network info"

    if deploy_cfme:
        assert dep_api.set_install_location_cfme(cfme_install_loc), \
            "Unable to set the CFME install location"
        # "Setting info for a Cloudforms Deployment"
        # "Setting CFME passwords"
        assert dep_api.set_creds_cfme(cfme_root_password), "Failed to set cfme root password"
        # "Unable to set the CFME passwords")

    deployment_attach_subscriptions(
        dep_api, rhn_username, rhn_password, rhn_sma_uuid, ose_sub_pool_name, ose_sub_quantity)

    dep_validation = dep_api.get_deployment_validation()['validation']

    if deploy_osp:
        # Sync with overcloud so we don't clobber any values that are set by fusor (overcloud admin pw)
        # "Syncing OpenStack data with fusor"
        dep_api.sync_openstack()

    assert not dep_validation['errors'], ("Validation contains errors:\n{}".format(
        '\n'.join(dep_validation['errors'])))

    assert dep_api.deploy(), "API deployment failed: {}".format(dep_api.last_response.text)


# TODO: This should be generic for any type of deployment
def test_api_deployment_success(dep_api, variables, deployment_name):
    """
    Query the fusor deployment object for the status of the Deploy task
    """
    if deployment_name:
        dep_api.load_deployment(deployment_name)

    dep = variables['deployment']

    deployment_time = 0
    deployment_time_wait = 1  # Time (minutes) to wait between polling for progress
    deployment_time_max = dep.get('deployment_timeout', 240)
    deployment_success = False
    fail_message = "Deployment timed out after {} hours".format(deployment_time_max / 60)
    # Wait a while for the deployment to complete (or fail),

    while not deployment_success and deployment_time < deployment_time_max:
        deployment_time += deployment_time_wait
        sleep(deployment_time_wait * 60)
        progress = dep_api.get_deployment_progress()
        dep_api.refresh_deployment_info()

        if(progress['result'] == 'success' and
           progress['state'] == 'stopped' and
           progress['progress'] == 1.0):
            deployment_success = True
            print 'API Deployment Succeeded!'
        elif progress['result'] == 'error' and progress['state'] == 'paused':
            deployment_success = False
            deployment_task_uuid = dep_api.fusor_data['deployment']['foreman_task_uuid']
            foreman_task = next(
                task for task in dep_api.fusor_data['foreman_tasks'] if(
                    task['id'] == deployment_task_uuid))

            # Loop through all sub tasks until we find one paused w/ error
            for sub_task in foreman_task['sub_tasks']:
                if sub_task['result'] == 'error':
                    sub_task_info = dep_api.foreman_task(sub_task['id'])['foreman_task']
                    fail_message = 'Deployment Failed: {} -> {}'.format(
                        sub_task_info['label'], sub_task_info['humanized_errors'])
                    assert deployment_success, fail_message

            # If we got here then the logic for finding the failed task needs to be fixed
            fail_message = "Unable to find the failed subtask for task: {}".format(
                '\n'.join([step['action_class'] for step in foreman_task['failed_steps']]))

            assert deployment_success, fail_message

    assert deployment_success, "DEFAULT: {}".format(fail_message)
