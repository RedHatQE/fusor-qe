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
def rhv_api(fusor_admin_username, fusor_admin_password, base_url):
    """
    RHEVFusorApi object with methods for accessing/editing RHEV deployment objects
    """
    fusor_ip = parse_ip_from_url(base_url)
    return fusor_api.RHEVFusorApi(fusor_ip, fusor_admin_username, fusor_admin_password)


def deployment_attach_sub(
        rhv_api, rhn_username, rhn_password, rhn_sma_uuid, sub_name, sub_quantity, **kwargs):
    """
    Attach the specified subscriptions to the deployment loaded in the rhv_api object

    attach_subs must be a list of dictionaries with each item having the following keys
    {
      name - Name of the subscription
      pool_id - uuid of the pool to attach
      quantity - Quantity of subs needed for this deployment.
    }
    """

    rhv_api.rhn_login(rhn_username, rhn_password)
    consumer = rhv_api.rhn_get_consumer(rhn_sma_uuid)
    rhv_api.rhn_set_upstream_consumer(consumer['name'], consumer['uuid'])
    subscriptions = rhv_api.rhn_get_consumer_subscriptions(rhn_sma_uuid)

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
                rhv_api.rhn_attach_subscription(
                    consumer['uuid'], pool_id, qty_additional)


def get_sma_uuid(rhv_api, rhn_username, rhn_password, sma_name):
    rhv_api.rhn_login(rhn_username, rhn_password)
    owner = rhv_api.rhn_owner_info(rhn_username)
    consumers = rhv_api.rhn_list_consumers(owner['key'])

    sma_uuid = None
    for consumer in consumers:
        if consumer['name'] == sma_name:
            sma_uuid = consumer['uuid']
            break

    return sma_uuid


def test_rhv_api(rhv_api, variables, deployment_name):
    dep = variables['deployment']
    dep_rhv = dep['products']['rhv']
    dep_cfme = dep['products']['cfme']
    dep_ose = dep['products']['ose']
    dep_sat = dep['products']['sat']

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
    deploy_cfme = 'cfme' in dep['install']
    deploy_ose = 'ocp' in dep['install']
    rhev_admin_password = dep_rhv['rhvm_adminpass']
    cfme_root_password = dep_cfme['cfme_admin_password']
    if not deployment_name:
        deployment_name = 'pytest-rhv-api-{}{}{}'.format(
            dep['deployment_id'], '-cfme' if deploy_cfme else '', '-ocp' if deploy_ose else '')
    deployment_desc = 'Pytest of the fusor api for deploying RHEV'

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
    ose_export_path = dep_ose['storage_path']
    ose_username = dep_ose['username']
    ose_user_password = dep_ose['user_password']
    ose_subdomain_name = dep_ose['subdomain_name'] if dep_ose['subdomain_name'] else dep['deployment_id']
    ose_sample_app_name = 'openshift_sample_helloworld'
    ose_sample_apps = dep_ose['sample_apps']  # List of sample apps to include in the deployment
    rhn_username = variables['credentials']['cdn']['username']
    rhn_password = variables['credentials']['cdn']['password']
    rhn_sma_uuid = dep_sat['rhsm_satellite']['uuid']
    ose_sub_pool_name = dep_ose['subscription']['name']
    ose_sub_quantity = dep_ose['subscription']['quantity']

    # "Creating RHEV deployment: {}".format(deployment_name)
    assert rhv_api.create_deployment(
        deployment_name, deployment_desc,
        deploy_cfme=deploy_cfme, deploy_ose=deploy_ose), "Unable to create RHEV deployment ({})".format(deployment_name)

    # log.info("Assigning RHEV Hypervisors: {}".format(rhevh_macs))
    assert rhv_api.set_discovered_hosts(rhevh_macs, rhevm_mac), "Unable to set the RHEV Hosts"

    # log.info("Setting the RHEV credentials")
    assert rhv_api.set_creds_rhev(rhev_admin_password), "Unable to set RHEV credentials"

    # Set NFS for CloudForms or OpenShift
    # log.info("Setting NFS storage values")
    assert rhv_api.set_nfs_storage(
        data_name, data_address, data_path,
        export_name, export_address, export_path,
        selfhosted_name, selfhosted_address, selfhosted_path), "Unable to set the NFS storage for the deployment"

    if deploy_cfme:
        # log.info("Setting info for a Cloudforms Deployment")
        # log.info("Setting CFME root/admin password")
        assert rhv_api.set_creds_cfme(cfme_root_password), "Unable to set the CFME root/admin passwords"

    if deploy_ose:
        # log.info("Setting info for a OpenShift Deployment")
        # log.info("Setting Master({}) node specs: vcpu({}), ram({}), disk size({})".format(
        #   ose_number_master_nodes,
        #   ose_master_vcpu,
        #   ose_master_ram,
        #   ose_master_disk))
        assert rhv_api.ose_set_master_node_specs(
            ose_number_master_nodes,
            ose_master_vcpu,
            ose_master_ram,
            ose_master_disk), 'Unable to set the OpenShift master node specs'

        # log.info("Setting Worker({}) node specs: vcpu({}), ram({}), disk size({})".format(
        #     ose_number_worker_nodes,
        #     ose_node_vcpu,
        #     ose_node_ram,
        #     ose_node_disk))
        assert rhv_api.ose_set_worker_node_specs(
            ose_number_worker_nodes,
            ose_node_vcpu,
            ose_node_ram,
            ose_node_disk), 'Unable to set the OpenShift worker node specs'

        assert rhv_api.ose_set_storage_size(ose_storage_size), 'Unable to set the OpenShift storage size for docker to {}'.format(ose_storage_size)

        # log.info("Setting NFS info:\nName: {} = -1\nHost: {}\nPath: {}".format(
        #     ose_storage_name,
        #     ose_storage_host,
        #     ose_export_path))
        assert rhv_api.set_ose_nfs_storage(
            ose_storage_name,
            ose_storage_host,
            ose_export_path), 'Unable to set the OpenShift NFS storage'

        # log.info("Setting OpenShift credentials: {}/{}".format(
        #     ose_username,
        #     ose_user_password))
        assert rhv_api.set_ose_creds(ose_username, ose_user_password), 'Unable to set the OpenShift credentials'

        # log.info("Setting OpenShift subdomain: {}".format(ose_subdomain_name))
        assert rhv_api.set_ose_subdomain(ose_subdomain_name), 'Unable to set the OpenShift subdomain name'

        if ose_sample_apps:
            # log.info("Enabling OpenShift sample applications")
            for app in ose_sample_apps:
                # Do some translation since the yaml app name value defaults to the element id
                if 'hello_world' in app:
                    assert rhv_api.set_deployment_property(
                        ose_sample_app_name, True), 'Unable to enable OpenShift sample application hello_world'

    deployment_attach_sub(
        rhv_api, rhn_username, rhn_password, rhn_sma_uuid, ose_sub_pool_name, ose_sub_quantity)

    # log.info("Starting RHEV deployment")
    assert rhv_api.deploy()


# TODO: This should be generic for any type of deployment
def test_rhv_api_deployment_success(rhv_api, variables, deployment_name):
    """
    Query the fusor deployment object for the status of the Deploy task
    """
    if deployment_name:
        rhv_api.load_deployment(deployment_name)

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
        progress = rhv_api.get_deployment_progress()
        rhv_api.refresh_deployment_info()

        if(progress['result'] == 'success' and
           progress['state'] == 'stopped' and
           progress['progress'] == 1.0):
            deployment_success = True
            print 'OpenStack Deployment Succeeded!'
        elif progress['result'] == 'error' and progress['state'] == 'paused':
            deployment_success = False
            deployment_task_uuid = rhv_api.fusor_data['deployment']['foreman_task_uuid']
            foreman_task = next(
                task for task in rhv_api.fusor_data['foreman_tasks'] if(
                    task['id'] == deployment_task_uuid))

            # Loop through all sub tasks until we find one paused w/ error
            for sub_task in foreman_task['sub_tasks']:
                if sub_task['result'] == 'error':
                    sub_task_info = rhv_api.foreman_task(sub_task['id'])['foreman_task']
                    fail_message = 'Deployment Failed: {} -> {}'.format(
                        sub_task_info['label'], sub_task_info['humanized_errors'])
                    assert deployment_success, fail_message

            # If we got here then the logic for finding the failed task needs to be fixed
            fail_message = "Unable to find the failed subtask for task: {}".format(
                '\n'.join([step['action_class'] for step in foreman_task['failed_steps']]))

            assert deployment_success, fail_message

    assert deployment_success, "DEFAULT: {}".format(fail_message)
