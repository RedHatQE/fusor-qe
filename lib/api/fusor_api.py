import requests
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning

"""
Disable all notices InsecureRequestWarning
InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.org/en/latest/security.html
  InsecureRequestWarning)
"""
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class FusorApi(object):
    def __init__(self, fusor_ip, user, pw):
        self.fusor_ip = fusor_ip
        self.fusor_api_url = "https://{}/fusor/api/v21/".format(self.fusor_ip)
        self.foreman_api_url = "https://{}/api/v21/".format(self.fusor_ip)
        self.customer_api_url = "https://{}/customer_portal/".format(self.fusor_ip)
        self.username = user
        self.password = pw
        # We need to use a persistent session when logging in with Red Hat Network info
        # TODO: Replace requests calls with sessions throughout fusor API
        self.customer_session = None
        # Save the response data just in case we need to review the HTTP data returned
        self.last_response = None

    def _fusor_get_resource(self, resource):
        self.last_response = requests.get(
            "{}{}".format(self.fusor_api_url, resource),
            auth=(self.username, self.password), verify=False)
        return self.last_response

    def _foreman_get_resource(self, resource):
        self.last_response = requests.get(
            "{}{}".format(self.foreman_api_url, resource),
            auth=(self.username, self.password), verify=False)
        return self.last_response

    def _fusor_put_resource(self, resource, data):
        self.last_response = requests.put(
            "{}{}".format(self.fusor_api_url, resource), json=data,
            auth=(self.username, self.password), verify=False)
        return self.last_response

    def _fusor_post_resource(self, resource, data):
        self.last_response = requests.post(
            "{}{}".format(self.fusor_api_url, resource), json=data,
            auth=(self.username, self.password), verify=False)
        return self.last_response

    def _fusor_delete_resource(self, resource, data):
        self.last_response = requests.delete(
            "{}{}".format(self.fusor_api_url, resource), json=data,
            auth=(self.username, self.password), verify=False)
        return self.last_response

    def _customer_get_resource(self, resource):
        self.last_response = self.customer_session.get(
            "{}{}".format(self.customer_api_url, resource),
            auth=(self.username, self.password), verify=False)
        return self.last_response

    def _customer_put_resource(self, resource, data):
        self.last_response = self.customer_session.put(
            "{}{}".format(self.customer_api_url, resource), json=data,
            auth=(self.username, self.password), verify=False)
        return self.last_response

    def _customer_post_resource(self, resource, data):
        self.last_response = self.customer_session.post(
            "{}{}".format(self.customer_api_url, resource), json=data,
            auth=(self.username, self.password), verify=False)
        return self.last_response

    def _upload_manifest(self, deployment_id, manifest_file):
        """
        Upload a manifest file for the specified deployment
        """
        data = {
            "manifest_file": {
                "deployment_id": deployment_id,
                "file": manifest_file, }, }

        resource = "subscriptions/{}/upload".format(deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return None

        return response.json()

    def list_deployments(self):

        return self._fusor_get_resource('deployments').json()['deployments']

    def deployment_id(self, name):
        """
        Given a deployment name, returns its id. Returns None if name isn't found.
        :param name: name of deployment
        :return: id of deployment
        """
        for d in self.list_deployments():
            if d['name'] == name:
                return d['id']
        else:
            return None

    def deployment(self, deployment_id):
        """
        Given the deployment id, return the deployment as a dictionary
        :param deployment_id:
        :return:
        """
        return self._fusor_get_resource('deployments/{}'.format(deployment_id)).json()

    def foreman_task(self, task_uuid):
        """
        Given a foreman uuid, return the associated task
        :param task_uuid:
        :return: dictionary of foreman task
        """
        return self._foreman_get_resource('foreman_tasks/{}'.format(task_uuid)).json()

    def get_deployment_log(self, deployment_id):
        """
        Retrieve the log of this deployment
        """
        return self._fusor_get_resource('deployments/{}/log'.format(deployment_id)).json()

    def get_deployment_progress(self, deployment_id):
        dep = self.deployment(deployment_id)
        deploy_task = self.foreman_task(dep['deployment']['foreman_task_uuid'])['foreman_task']

        result = {
            "progress": deploy_task['progress'],
            "state": deploy_task['state'],
            "result": deploy_task['result'],
            "started_at": deploy_task['started_at'],
            "id": deploy_task['id'],
            "label": deploy_task['label'],
        }

        return result

    def get_discovered_hosts(self, host_id=None):
        """
        Get a list of the foreman discovery hosts.  If host_id exists then retrieve a single host
        host_id
        """

        resource = "discovered_hosts" + ("/" + host_id if host_id else "")
        response = self._foreman_get_resource(resource)

        if response.status_code != 200:
            return None

        return response.json()

    def get_subscriptions(self, deployment_id):
        """
        Retrieve the subscriptions for a deployment
        """

        response = self._fusor_get_resource("subscriptions?deployment=".format(deployment_id))

        if response.status_code != 200:
            return None

        return response.json()['subscriptions']

    def get_deployment_validation(self, deployment_id):
        """
        Return any warnings or errors associated with this deployment
        """
        resource = "deployments/{}/validate".format(deployment_id)
        response = self._fusor_get_resource(resource)

        return response.json()

    def rhn_login(self, username, password):
        """
        Login to RHN account via Satellite
        """

        self.customer_session = requests.Session()
        data = {"username": username, "password": password}
        response = self._customer_post_resource("login", data)

        if response.status_code != 200:
            return False

        return True

    def rhn_logout(self):
        """
        Logout of RHN account via Satellite
        """

        data = {}
        response = self._customer_post_resource("logout", data)

        self.customer_session.close()
        self.customer_session = None

        if response.status_code != 200:
            return False

        return True

    def rhn_owner_info(self, rhn_username):
        """
        Retrieve the owner information from the customer portal
        """
        if self.customer_session is None:
            raise Exception("No customer login session has been created")

        resource = "users/{}/owners".format(rhn_username)
        response = self._customer_get_resource(resource)

        if response.status_code != 200:
            return None

        # There is only 1 owner
        return response.json().pop()

    def rhn_list_consumers(self, rhn_owner_key):
        """
        List the Satellite consumers (aka "Subscription Application Managers")
        that already exist on the account.
        """

        if self.customer_session is None:
            raise Exception("No customer login session has been created")

        resource = "owners/{}/consumers?type=satellite".format(rhn_owner_key)
        response = self._customer_get_resource(resource)

        if response.status_code != 200:
            return None

        return response.json()

    def rhn_get_consumer(self, consumer_uuid):
        """
        Retrieve a Satellite consumers (aka "Subscription Application Managers")
        """

        if self.customer_session is None:
            raise Exception("No customer login session has been created")

        resource = "consumers/{}".format(consumer_uuid)
        response = self._customer_get_resource(resource)

        if response.status_code != 200:
            return None

        return response.json()

    def rhn_attach_subscription(self, consumer_uuid, sub_pool_id, quantity_to_add):
        """
        Attach a subscription to the specified consumer
        """

        if self.customer_session is None:
            raise Exception("No customer login session has been created")

        resource = "consumers/{}/entitlements?pool={}&quantity={}".format(
            consumer_uuid, sub_pool_id, quantity_to_add)
        data = {}
        response = self._customer_post_resource(resource, data)

        if response.status_code != 200:
            return None

        return response.json()

    def rhn_unattach_subscription(self, consumer_uuid, sub_pool_id):
        """
        Unattach a subscription from the specified consumer
        """

        if self.customer_session is None:
            raise Exception("No customer login session has been created")

        resource = "consumers/{}?pool={}".format(
            consumer_uuid, sub_pool_id)
        response = self._customer_post_resource(resource)

        if response.status_code != 200:
            return None

        return response.json()

    def rhn_get_subscriptions(self, consumer_uuid):
        """
        Retrieve a Satellite consumers (aka "Subscription Application Managers") available
        subscriptions
        """

        if self.customer_session is None:
            raise Exception("No customer login session has been created")

        resource = "pools?consumer={}&listall=false".format(consumer_uuid)
        response = self._customer_get_resource(resource)

        if response.status_code != 200:
            return None

        return response.json()

    def rhn_get_consumer_subscriptions(self, consumer_uuid):
        """
        Retrieve a Satellite consumers (aka "Subscription Application Managers") subscriptions
        """

        if self.customer_session is None:
            raise Exception("No customer login session has been created")

        resource = "consumers/{}/entitlements".format(consumer_uuid)
        response = self._customer_get_resource(resource)

        if response.status_code != 200:
            return None

        return response.json()

    def add_deployment_subscription(
            self, deployment_id, contract_number, product_name, quantity_attached,
            start_date, end_date, total_quantity, source="added", quantity_to_add=0):
        """
        Add a subscription to the deployment specified
        """
        data = {
            "subscription": {
                "deployment_id": deployment_id,
                "contract_number": contract_number,
                "product_name": product_name,
                "quantity_attached": quantity_attached,
                "start_date": start_date,
                "end_date": end_date,
                "total_quantity": total_quantity,
                "source": source,
                "quantity_to_add": quantity_to_add, }}

        resource = "subscriptions"
        response = self._fusor_post_resource(resource, data)

        return response

        if response in [200, 202]:
            return False

        return True


class QCIDeploymentApi(FusorApi):
    """
    This class handles the deployment of all products supported by QCI using
    the fusor API
    """
    def __init__(self, fusor_ip, user, pw):
        super(QCIDeploymentApi, self).__init__(fusor_ip, user, pw)
        self.fusor_data = None
        self.deployment_id = None
        self.install_location_cfme = None
        self.install_location_ocp = None
        self.openstack_api_url = "https://{}/fusor/api/openstack/deployments/".format(self.fusor_ip)
        # Id for deployment objects specific to the orchestration of an openstack deployment
        # This will also be stored in fusor deployment object 'openstack_deployment_id'
        self.openstack_deployment_id = None

    ################################################################################################
    # Private Helper Methods
    ################################################################################################
    def _openstack_get_resource(self, resource):
        self.last_response = requests.get(
            "{}{}".format(self.openstack_api_url, resource),
            auth=(self.username, self.password), verify=False)
        return self.last_response

    def _openstack_put_resource(self, resource, data):
        self.last_response = requests.put(
            "{}{}".format(self.openstack_api_url, resource), json=data,
            auth=(self.username, self.password), verify=False)
        return self.last_response

    def _openstack_post_resource(self, resource, data):
        self.last_response = requests.post(
            "{}{}".format(self.openstack_api_url, resource), json=data,
            auth=(self.username, self.password), verify=False)
        return self.last_response

    def _openstack_delete_resource(self, resource, data):
        self.last_response = requests.delete(
            "{}{}".format(self.openstack_api_url, resource), json=data,
            auth=(self.username, self.password), verify=False)
        return self.last_response

    ################################################################################################
    # Public Helper Methods
    ################################################################################################

    def create_deployment(
            self, name, description=None,
            deploy_rhv=False, deploy_osp=False,
            deploy_cfme=False, deploy_ose=False,
            organization_id='1', lifecycle_environment_id=None, access_insights=False):
        """
        Create a new deployment with the products specified and store the
        deployment data returned
        NOTE: RHCI currently only supports the Default organization
        """
        data = {'deployment': {
            'name': name,
            'description': description,
            'deploy_rhev': deploy_rhv,
            'deploy_cfme': deploy_cfme,
            'deploy_openshift': deploy_ose,
            'deploy_openstack': deploy_osp,
            'organization_id': organization_id,
            'lifecycle_environment_id': lifecycle_environment_id,
            'enable_access_insights': access_insights, }, }
        response = self._fusor_post_resource('deployments', data)

        if response.status_code != 200:
            return False

        self.fusor_data = {}
        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        self.deployment_id = self.fusor_data['deployment']['id']

        return True

    def deploy(self):
        """
        Start the deployment Requires an active Red Hat customer portal session
        """
        if not self.deployment_id:
            raise Exception("Unable to deploy because there is no deployment id")

        if not self.customer_session:
            raise Exception("Please login to the Red Hat customer portal")

        validation = self.get_deployment_validation()

        if validation['validation']['errors']:
            return False

        resource = "deployments/{}/deploy".format(self.deployment_id)
        data = {}

        response = self.customer_session.put(
            "{}{}".format(self.fusor_api_url, resource), json=data,
            auth=(self.username, self.password), verify=False)

        self.fusor_data['deploy_task'] = None

        if response.status_code not in [200, 202]:
            return False

        # /deploy doesn't return a nested dict so we need to nest the data
        self.fusor_data['deploy_task'] = response.json()

        return True

    def redeploy(self):
        """
        Redeploy this deployment so the deployment can deploy successfully :)
        """
        if not self.deployment_id:
            raise Exception("Unable to redeploy because there is no fusor data")

        if not self.customer_session:
            raise Exception("Please login to the Red Hat customer portal")

        resource = "deployments/{}/redeploy".format(self.deployment_id)
        data = {}

        # TODO: Replace requests calls with sessions throughout fusor API

        response = self.customer_session.put(
            "{}{}".format(self.fusor_api_url, resource), json=data,
            auth=(self.username, self.password), verify=False)

        if response.status_code not in [200, 202]:
            return False

        self.fusor_data['deploy_task'] = response.json()

        return True

    def load_deployment(self, name):
        """
        Load the data for an existing deployment with the given name
        Return True if successful
        """
        deployments = self.list_deployments()
        if deployments is None:
            return False

        self.fusor_data = {}

        for deployment in deployments:
            if deployment['name'] == name:
                # Load all of the fusor info about the deployment
                self.fusor_data = self.deployment(deployment['id'])
                self.deployment_id = deployment['id']
                self.openstack_deployment_id = deployment['openstack_deployment_id']
                return True

        return False

    def refresh_deployment_info(self):
        """
        Refresh the local deployment info with what is on the fusor server
        """
        if not self.deployment_id:
            raise Exception("Unable to update deployment because there is no deployment id")

        dep = self.deployment(self.deployment_id)

        if not dep:
            return False

        for key in dep:
            self.fusor_data[key] = dep[key]

        return True

    def _remove_duplicate_keys(self):
        """
        Remove any keys that are duplicated in the fusor api before updating
        """
        pass

    def delete_deployment(self):
        """
        Delete the currently loaded deployment from Satellite
        """
        if not self.deployment_id:
            raise Exception("Unable to delete deployment because there is no deployment id")

        resource = 'deployments/{}'.format(self.deployment_id)
        data = {}
        response = self._fusor_delete_resource(resource, data)

        if response.status_code != 200:
            return False

        self.fusor_data = None

        return True

    def update_foreman_task(self, task_uuid):
        """
        THIS IS A HACK!!!!!
        We need to save the task uuid returned by /deploy back into the deploy object
        See - RHCIDEV Trello Card: https://trello.com/c/Gz0HABHv
        When this card is complete then we should be able to delete it
        """
        if not self.deployment_id:
            raise Exception("Unable to send deployment data because there is no deployment id")

        resource = 'deployments/{}'.format(self.fusor_data['deployment']['id'])
        data = {
            'deployment': {
                'has_content_error': False,
                'foreman_task_uuid': task_uuid, }}

        response = self._fusor_put_resource(resource, data)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def update_deployment(self):
        if not self.deployment_id:
            raise Exception("Unable to update deployment data because there is no deployment id")

        if not self.fusor_data:
            raise Exception("Unable to update deployment because there is no fusor deployment data")

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, {'deployment': self.fusor_data['deployment']})

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def set_disconnected(self, manifest_file, cdn_url):
        """
        Sets disconnected mode by uploading a manifest and populating the cdn
        DOESN'T WORK ...YET
        """
        raise NotImplementedError("Disconnected mode doesn't work yet")

        if not self.deployment_id:
            raise Exception(
                "Unable to set disconnected mode because there is no deployment id")

        # TODO: Upload the file to the server and just fill out the yaml
        if not self._upload_manifest(self.deployment_id, manifest_file):
            return False

        self.fusor_data['deployment']['cdn_url'] = cdn_url
        self.fusor_data['deployment']['is_disconnected'] = True
        subscriptions = self.get_subscriptions(self.deployment_id)
        self.fusor_data['deployment']['subscription_ids'] = []
        # Import imported subscriptions ...BA-DA-BUM
        for sub in subscriptions:
            if sub['source'] == 'imported':
                self.fusor_data['deployment']['subscription_ids'].append(sub['id'])

        return len(self.fusor_data['deployment']['subscription_ids']) > 0

    def add_deployment_subscription(
            self, contract_number, product_name, quantity_attached,
            start_date, end_date, total_quantity, source="added", quantity_to_add=0):

        if not self.deployment_id:
            raise Exception("Unable to update deployment because there is no deployment id")

        return super(FusorApi, self).add_deployment_subscription(
            self.deployment_id, contract_number, product_name, quantity_attached,
            start_date, end_date, total_quantity, source, quantity_to_add)

    def rhn_set_upstream_consumer(self, name, uuid):
        """
        Set the upstream consumer information for this deployment
        """
        if not self.deployment_id:
            raise Exception("Unable to update deployment because there is no deployment id")

        data = {'deployment': {
            'upstream_consumer_name': name,
            'upstream_consumer_uuid': uuid, }}

        resource = "deployments/{}".format(self.deployment_id)

        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def get_deployment_validation(self):
        """
        Return any warnings or errors associated with this deployment
        """
        if not self.deployment_id:
            raise Exception("Unable to update deployment because there is no deployment id")

        resource = "deployments/{}/validate".format(self.deployment_id)
        response = self._fusor_get_resource(resource)

        if response.status_code not in [200, 202]:
            return None

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return response.json()

    def get_deployment_progress(self):
        if not self.deployment_id:
            raise Exception("Unable to update deployment because there is no deployment id")

        return super(FusorApi, self).get_deployment_progress(self.deployment_id)

    def get_deployment_log(self):
        """
        Retrieve the log of this deployment
        """
        if not self.deployment_id:
            raise Exception("Unable to retrieve the log because there is no deployment id")

        self.fusor_data['fusor_log'] = None

        response = self._fusor_get_resource('deployments/{}/log'.format(
            self.deployment_id))

        if response.status_code in [200, 202]:
            response_data = response.json()
            self.fusor_data[u'fusor_log'] = response_data['fusor_log']

        return self.fusor_data['fusor_log']

    def set_deployment_property(self, property_name, property_value):
        """
        Set a deployment object property directly. This is a helper function to update individual
        properties that aren't logically grouped with other actions.
        This is restricted to immediate children of the deployment object and will overwrite
         the value of the specified property.

        Args:
        - property_name: name of the property you want to set
        - value: value of the property
        """
        data = {'deployment': {
            property_name: property_value, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    ################################################################################################
    # OpenShift Methods
    ################################################################################################
    def ose_set_storage_size(self, disk_size):
        """
        Set the disk size of OpenShift docker storage.  This will be the 2nd hard drive for the
        OSE nodes
        """

        data = {'deployment': {
            'openshift_storage_size': disk_size, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def ose_set_master_node_specs(self, master_node_count, master_vcpu, master_ram, master_disk):
        """
        Set the master node count and specs for each master node
        """
        if not self.deployment_id:
            raise Exception(
                "Unable to set OpenShift master node specs "
                "because there is no deployment id")

        return self._ose_set_node_specs(
            "openshift_number_master_nodes", master_node_count,
            "openshift_master_vcpu", master_vcpu,
            "openshift_master_ram", master_ram,
            "openshift_master_disk", master_disk)

    def ose_set_worker_node_specs(self, worker_node_count, worker_vcpu, worker_ram, worker_disk):
        """
        Set the worker node count and specs for each worker node
        """
        if not self.deployment_id:
            raise Exception(
                'Unable to set OpenShift worker node specs '
                'because there is no deployment id')

        return self._ose_set_node_specs(
            'openshift_number_worker_nodes', worker_node_count,
            'openshift_node_vcpu', worker_vcpu,
            'openshift_node_ram', worker_ram,
            'openshift_node_disk', worker_disk)

    def _ose_set_node_specs(
            self,
            node_count_name, node_count,
            node_vcpu_name, node_vcpu,
            node_ram_name, node_ram,
            node_disk_name, node_disk):
        """
        Set the node specs.
        Helper function since master nodes set the same number and type of objects
        """
        data = {'deployment': {
            node_count_name: node_count,
            node_vcpu_name: node_vcpu,
            node_ram_name: node_ram,
            node_disk_name: node_disk, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def set_install_location_ocp(self, location=None):
        """
        Set the location where OpenShift will be deployed.

        location - can be either 'rhv' or 'osp'
        """

        location_dict = {
            'rhv': 'RHEV',
            'osp': 'OpenStack', }

        if not location or location.lower() not in ['rhv', 'osp']:
            raise Exception('Location for OpenShift ({}) is invalid'.format(location))

        self.install_location_ocp = location_dict[location.lower()]

        data = {
            "deployment": {
                'openshift_install_loc': self.install_location_ocp, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def set_ose_nfs_storage(self, storage_name, storage_host, storage_path):
        """
        Set the nfs storage options for OpenShift
        """
        if not self.deployment_id:
            raise Exception(
                'Unable to set nfs storage for RHEV because there is no deployment id')

        data = {
            'deployment': {
                'openshift_storage_type': 'NFS',
                'openshift_storage_name': storage_name,
                'openshift_storage_host': storage_host,
                'openshift_export_path': storage_path, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def set_ose_creds(self, username, pw):
        """
        Set the OpenShift credentials
        """
        if not self.deployment_id:
            raise Exception("Unable to set the OpenShift creds because there is no deployment id")

        data = {
            "deployment": {
                'openshift_username': username,
                'openshift_user_password': pw,
                'openshift_root_password': pw, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def set_ose_subdomain(self, subdomain_name):
        """
        Set the OpenShift subdomain
        """
        if not self.deployment_id:
            raise Exception(
                "Unable to set the OpenShift subdomain because "
                "there is no deployment id")

        data = {
            "deployment": {
                'openshift_subdomain_name': subdomain_name, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    ################################################################################################
    # CloudForms Methods
    ################################################################################################
    def set_creds_cfme(self, pw):
        """
        Set the CFME credentials
        """
        if not self.deployment_id:
            raise Exception("Unable to update deployment because there is no deployment id")

        data = {
            "deployment": {
                'cfme_root_password': pw,
                'cfme_admin_password': pw,
                'cfme_db_password': pw, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def set_install_location_cfme(self, location=None):
        """
        Set the location where CloudForms will be deployed.

        location - can be either 'rhv' or 'osp'
        """

        location_dict = {
            'rhv': 'RHEV',
            'osp': 'OpenStack', }

        if not location or location.lower() not in ['rhv', 'osp']:
            raise Exception('Location for CloudForms ({}) is invalid'.format(location))

        self.install_location_cfme = location_dict[location.lower()]

        data = {
            "deployment": {
                'cfme_install_loc': self.install_location_cfme, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    ################################################################################################
    # RHV Methods
    ################################################################################################
    def rhv_is_self_hosted(self):
        if not self.fusor_data.get('deployment'):
            raise Exception("There is no fusor deployment data")

        return self.fusor_data['deployment']['rhev_is_self_hosted']

    def set_rhv_hosts(self, rhvh_macs, rhvm_mac=None, naming_scheme='Freeform'):
        """
        Set the hypervisor hosts (and RHEV engine). If rhevm mac is None then deploy self hosted
        rhvh_macs - (List of Strings) hypervisor macs
        rhvm_mac - (String) engine mac OPTIONAL
        """

        if not self.deployment_id:
            raise Exception("Unable to update deployment because there is no deployment id")

        # Wrap string in a list
        if type(rhvh_macs) is str:
            rhvh_macs = [rhvh_macs]

        # Grab a list of discovered hosts
        disco_hosts = self.get_discovered_hosts().get(
            'discovered_hosts', [])

        engine_id = None
        hypervisor_ids = []

        for host in disco_hosts:
            if host['mac'] == rhvm_mac:
                engine_id = host['id']
            elif host['mac'] in rhvh_macs:
                hypervisor_ids.append(host['id'])

        if (rhvm_mac and (not engine_id)) and not hypervisor_ids:
            return False

        data = {
            "deployment": {
                'rhev_is_self_hosted': engine_id is None,
                'host_naming_scheme': naming_scheme,
                'rhev_engine_host_id': engine_id,
                'discovered_host_ids': hypervisor_ids, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def rhv_set_creds(self, pw):
        """
        Set the RHV admin/root password
        """
        if not self.deployment_id:
            raise Exception("Unable to update deployment because there is no deployment id")

        data = {
            "deployment": {
                'rhev_engine_admin_password': pw,
                'rhev_root_password': pw, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def rhv_set_nfs_storage(
            self,
            data_name, data_address, data_path,
            export_name, export_address, export_path,
            hosted_storage_name=None, hosted_storage_address=None, hosted_storage_path=None,
            rhev_data_center_name='Default', rhev_cluster_name='Default'):
        """
        Set the nfs storage options for RHV.
        """
        if not self.deployment_id:
            raise Exception(
                "Unable to set nfs storage for RHEV because there is no deployment id")

        data = {
            "deployment": {
                'rhev_data_center_name': rhev_data_center_name,
                'rhev_cluster_name': rhev_cluster_name,
                'rhev_storage_type': 'NFS',
                'rhev_storage_name': data_name,
                'rhev_storage_address': data_address,
                'rhev_share_path': data_path,
                'rhev_export_domain_name': export_name,
                'rhev_export_domain_address': export_address,
                'rhev_export_domain_path': export_path,
                'hosted_storage_name': hosted_storage_name,
                'hosted_storage_address': hosted_storage_address,
                'hosted_storage_path': hosted_storage_path, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code != 200:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    ################################################################################################
    # OpenStack Methods
    ################################################################################################
    def add_undercloud(self, ip, ssh_user, ssh_pass):
        if not self.deployment_id:
            raise Exception('Unable to add undercloud because there is no deployment id')

        # TODO: Verify if we need to pass the nested undercloud dict
        undercloud_data = {
            "undercloud_host": ip,
            "undercloud_user": ssh_user,
            "undercloud_password": ssh_pass, }

        resource = "{}/undercloud".format(self.deployment_id)
        response = self._openstack_post_resource(resource, undercloud_data)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def get_undercloud_status(self):
        if not self.deployment_id:
            raise Exception('Unable to get deployment id because there is no deployment id')

        response = self._openstack_get_resource("{0}/underclouds/{0}".format(
            self.deployment_id))

        if response.status_code not in [200, 202]:
            return False

        undercloud_status = response.json()

        return undercloud_status['deployed'] and (undercloud_status['failed'] is False)

    def get_introspection_tasks(self):
        """
        Retrieves the OpenStack introspection task currently running
        """
        if not self.deployment_id:
            raise Exception('Unable to get deployment id because there is no deployment id')

        resource = "{}/nodes/introspection_tasks".format(self.deployment_id)
        response = self._openstack_get_resource(resource)

        if response.status_code not in [200, 202]:
            return None

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return response_data

    def get_openstack_images(self):
        """
        Get a list of the OpenStack images
        """
        if not self.deployment_id:
            raise Exception('Unable to get deployment id because there is no deployment id')

        resource = "{}/images".format(self.deployment_id)
        response = self._openstack_get_resource(resource)

        if response.status_code not in [200, 202]:
            return None

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return response.json()

    def get_osp_nodes(self):
        """
        Get a list of the registered OpenStack nodes for this deployment
        """
        if not self.deployment_id:
            raise Exception('Unable to get deployment id because there is no deployment id')

        resource = "{0}/nodes".format(self.deployment_id)
        response = self._openstack_get_resource(resource)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return len(self.fusor_data['nodes']) > 0

    def register_osp_nodes(
            self, ipmi_driver, ipmi_ip, ipmi_user, ipmi_pass,
            node_mac, deploy_kernel_id, deploy_ramdisk_id, virt_type="virsh", capabilities="boot_option:local"):
        """
        Register the node with OSP using the specified ipmi interface
        You'll need to check the status of the introspection tasks to know if the nodes were
         registered successfully. Check task status using foreman tasks

        NOTE: Web UI passes extra keys below that don't seem to be necessary for external api use
        node->driver_info->deploy_kernel = "<OSP KERNEL UUID>"
        node->driver_info->deploy_ramdisk = "<OSP RAMDISK UUID>"
        node->properties->capabilities = "boot_option:local"
        """
        if not self.deployment_id:
            raise Exception('Unable to get deployment id because there is no deployment id')

        osp_node_data = {
            "node": {
                "driver": ipmi_driver,
                "driver_info": {
                    "ssh_address": ipmi_ip,
                    "ssh_username": ipmi_user,
                    "ssh_password": ipmi_pass,
                    "ssh_virt_type": "virsh",
                    "deploy_kernel": deploy_kernel_id,
                    "deploy_ramdisk": deploy_ramdisk_id,
                },
                "properties": {
                    "capabilities": capabilities,
                },

                "address": node_mac}, }

        resource = "{}/nodes".format(self.deployment_id)
        response = self._openstack_post_resource(resource, osp_node_data)

        if response.status_code not in [200, 202]:
            return False

        return True

    def wait_for_osp_node_registration(self, delay=10, maxtime=30, introspection_attempts_max=1):
        """
        Wait for node registration to finish processing either by success/error
        If fusor_data['introspection_tasks'] is empty, it will attempt to refresh the
         deployment info from the server
        Arguments:
          maxtime: Max time to wait in minutes
          delay: seconds to wait between checking tasks
           introspection_attempts_max: number of attempts refresh the introspection tasks if empty
        Return Value:
          dictionary[<node_uuid>] = True for success and false otherwise
        """
        if not self.deployment_id:
            raise Exception('Unable to get deployment id because there is no deployment id')

        if not self.fusor_data:
            raise Exception('Unable to wait for nodes because there is no fusor data')

        tasks_finished = False
        total_time = 0
        result_pending_value = 'pending'
        introspection_attempts = 0

        introspection_tasks = self.fusor_data['introspection_tasks']

        while ((introspection_attempts < introspection_attempts_max) and
               (len(introspection_tasks) < 1)):
                self.refresh_deployment_info()
                introspection_tasks = self.fusor_data['introspection_tasks']
                introspection_attempts += 1

        if len(introspection_tasks) < 1:
            self.refresh_deployment_info()
            introspection_tasks = self.fusor_data['introspection_tasks']

        while not tasks_finished:
            tasks = [
                self.foreman_task(t['task_id']) for t in introspection_tasks if(
                    t['deployment_id'] == self.deployment_id)]

            tasks_result = [t['foreman_task']['result'] != result_pending_value for t in tasks]

            tasks_finished = reduce(lambda x, y: x and y, tasks_result)

            sleep(delay)
            if (total_time * delay) >= (maxtime * 60):
                break

            total_time += 1

        return tasks_finished

    def set_overcloud_node_count(self, node_count):
        """
        Set the total number of nodes registered with the overcloud
        """
        if not self.openstack_deployment_id:
            raise Exception('Unable to update role because there is no openstack deployment id')

        data = {
            'openstack_deployment': {
                'overcloud_node_count': node_count,
            }, }

        resource = 'openstack_deployments/{}'.format(self.openstack_deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def get_overcloud_deployment_plan(self):
        """
        Get the Fusor deployment plan and save it in self.fusor_data
        Return True if sucessful
        """
        if not self.deployment_id:
            raise Exception('Unable to get deployment id because there is no deployment id')

        resource = '{}/deployment_plans/overcloud'.format(self.deployment_id)
        response = self._openstack_get_resource(resource)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def update_osp_role_compute(self, flavor, count):
        """
        Assign compute role the specified flavor and count
        """

        return self.update_osp_role(
            'overcloud_compute_flavor', flavor,
            'overcloud_compute_count', count)

    def update_osp_role_controller(self, flavor, count):
        """
        Assign controller role the specified flavor and count
        """

        return self.update_osp_role(
            'overcloud_controller_flavor', flavor,
            'overcloud_controller_count', count)

    def update_osp_role_ceph(self, flavor, count):
        """
        Assign ceph role the specified flavor and count
        """

        return self.update_osp_role(
            'overcloud_ceph_storage_flavor', flavor,
            'overcloud_ceph_count', count)

    def update_osp_role_cinder(self, flavor, count):
        """
        Assign cinder role the specified flavor and count
        """

        return self.update_osp_role(
            'overcloud_block_storage_flavor', flavor,
            'overcloud_block_count', count)

    def update_osp_role_swift(self, flavor, count):
        """
        Assign swift role the specified flavor and count
        """

        return self.update_osp_role(
            'overcloud_object_storage_flavor', flavor,
            'overcloud_object_count', count)

    def update_osp_role(self, flavor_role_name, flavor, count_role_name, count):
        """
        Assign a role count and flavor with one api call
        """
        if not self.openstack_deployment_id:
            raise Exception('Unable to update role because there is no openstack deployment id')

        data = {
            'openstack_deployment': {
                flavor_role_name: flavor,
                count_role_name: count,
            }, }

        resource = 'openstack_deployments/{}'.format(self.openstack_deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def update_osp_role_flavor(self, role_name, role_flavor):
        """
        Assign the OSP flavor to the specified role
        """
        if not self.deployment_id:
            raise Exception('Unable to get deployment id because there is no deployment id')

        resource = '{}/deployment_plans/overcloud/update_role_flavor'.format(self.deployment_id)
        data = {
            "role_name": role_name,
            "flavor_name": role_flavor, }

        response = self._openstack_put_resource(resource, data)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def update_osp_role_count(self, role_name, role_count):
        """
        Assign 'role_count' number of nodes to the specified OSP role
        """
        if not self.fusor_data:
            raise Exception('Unable to get deployment id because there is no deployment id')

        data = {
            "deployment": {
                role_name: role_count, }}

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def node_osp_flavors(self):
        """
        Retrieve the list of OSP node flavors
        """
        if not self.deployment_id:
            raise Exception('Unable to get deployment id because there is no deployment id')

        resource = "{}/flavors".format(self.deployment_id)
        response = self._openstack_get_resource(resource)

        if response.status_code not in [200, 202]:
            return False

        self.fusor_data['osp_flavors'] = response.json()['flavors']

        return True

    def set_creds_overcloud(self, pw):
        """
        Set the OSP admin password
        """
        if not self.deployment_id:
            raise Exception("Unable to update deployment because there is no deployment id")

        data = {
            'openstack_deployment': {
                'overcloud_password': pw, }}

        resource = 'openstack_deployments/{}'.format(self.openstack_deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def set_nova_libvirt_type(self, libvirt_type='kvm'):
        """
        Set the Overcloud Compute Libvirt Type
        Wrapper for heat template param 'Compute-1::NovaComputeLibvirtType'
        """
        if not self.deployment_id:
            raise Exception("Unable to update deployment because there is no deployment id")

        data = {
            'deployment': {
                'openstack_overcloud_libvirt_type': libvirt_type,
            }, }

        resource = 'deployments/{}'.format(self.deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def set_overcloud_nic(self, external_nic):
        """
        Set the Overcloud external network nic
        Wrapper for heat template param 'Controller-1::NeutronPublicInterface'
        """
        if not self.openstack_deployment_id:
            raise Exception("Unable to update deployment because there is no deployment id")

        data = {
            'openstack_deployment': {
                'overcloud_ext_net_interface': external_nic,
            }, }

        resource = 'openstack_deployments/{}'.format(self.openstack_deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def set_overcloud_network(self, private_cidr, float_cidr, float_gateway):
        """
        Set the Overcloud network info
        """
        if not self.openstack_deployment_id:
            raise Exception(
                "Unable to set overcloud network because there is no "
                "openstack deployment id")

        data = {
            "openstack_deployment": {
                'overcloud_address': None,
                'overcloud_private_net': private_cidr,
                'overcloud_float_gateway': float_gateway,
                'overcloud_float_net': float_cidr, }}

        resource = 'openstack_deployments/{}'.format(self.openstack_deployment_id)
        response = self._fusor_put_resource(resource, data)

        if response.status_code not in [200, 202]:
            return False

        response_data = response.json()
        for key in response_data:
            self.fusor_data[key] = response_data[key]

        return True

    def sync_openstack(self):
        """
        Tells fusor to sync the openstack parameters with the fusor database
        """
        if not self.openstack_deployment_id:
            raise Exception("Unable to sync openstack deployment because there is no "
                            "openstack deployment id")

        resource = "openstack_deployments/{}/sync_openstack".format(
            self.openstack_deployment_id)
        data = {}
        response = self._fusor_post_resource(resource, data)

        if response.status_code not in [200, 202]:
            return False

        return True
