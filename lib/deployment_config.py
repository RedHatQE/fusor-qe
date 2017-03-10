import yaml
from lib.deployment_configs.rhv import RHV
from lib.deployment_configs.satellite import Satellite
from lib.deployment_configs.cfme import CFME
from lib.deployment_configs.osp import OSP
from lib.deployment_configs.ocp import OCP

class DeploymentConfig(object):
    '''
    This class manages the configuration for a QCI deployment
    defined by a yaml file.
    '''

    def __init__(self, path='./variables.yaml'):
        with open(path, 'r') as conffile:
            conf = yaml.load(conffile)

        # Initialize RHV config structure:
        self.__init_rhv(conf['deployment']['products']['rhv'])

        # Initialize Satellite structure:
        self.__init_sat(conf['deployment']['products']['sat'])

        # Initialize CFME Structure
        self.__init_cfme(conf['deployment']['products']['cfme'])

        # Initialize OSP Structure
        self.__init_osp(conf['deployment']['products']['osp'])

        # Initialize OCP Structure
        self.__init_ocp(conf['deployment']['products']['ose'])

        self.products = conf['deployment']['install']
        self.deployment_id = conf['deployment']['deployment_id']
        self.credentials = conf['credentials']

    def __init_rhv(self, conf_dict):
        self.rhv = RHV()
        self.rhv.cluster_name = conf_dict['cluster_name']
        self.rhv.cpu_type = conf_dict['cpu_type']
        self.rhv.data_center_name = conf_dict['data_center_name']
        self.rhv.data_domain_address = conf_dict['data_domain_address']
        self.rhv.data_domain_name = conf_dict['data_domain_name']
        self.rhv.data_domain_share_path = conf_dict['data_domain_share_path']
        self.rhv.export_domain_address = conf_dict['export_domain_address']
        self.rhv.export_domain_name = conf_dict['export_domain_name']
        self.rhv.export_domain_share_path = conf_dict['export_domain_share_path']
        self.rhv.hypervisor_count = conf_dict['hypervisor_count']
        self.rhv.include = conf_dict['include']
        self.rhv.rhv_setup_type = conf_dict['rhv_setup_type']
        self.rhv.rhvh_hostname = conf_dict['rhvh_hostname']
        self.rhv.rhvh_macs = conf_dict['rhvh_macs']
        self.rhv.rhvm_adminpass = conf_dict['rhvm_adminpass']
        self.rhv.rhvm_engine = conf_dict['rhvm_engine']
        self.rhv.rhvm_hostname = conf_dict['rhvm_hostname']
        self.rhv.rhvm_hypervisors = conf_dict['rhvm_hypervisors']
        self.rhv.rhvm_mac = conf_dict['rhvm_mac']
        self.rhv.storage_type = conf_dict['storage_type']
        self.rhv.selfhosted_domain_name = conf_dict['selfhosted_domain_name']
        self.rhv.selfhosted_domain_address = conf_dict['selfhosted_domain_address']
        self.rhv.selfhosted_domain_share_path = conf_dict['selfhosted_domain_share_path']
        self.rhv.self_hosted_engine_hostname = conf_dict['self_hosted_engine_hostname']


    def __init_sat(self, conf_dict):
        self.sat = Satellite()
        self.sat.deploy_org = conf_dict['deploy_org']
        self.sat.disconnected_manifest = conf_dict['disconnected_manifest']
        self.sat.disconnected_url = conf_dict['disconnected_url']
        self.sat.enable_access_insights = conf_dict['enable_access_insights']
        self.sat.env_path = conf_dict['env_path']
        self.sat.rhsm_subs = conf_dict['rhsm_subs']
        self.sat.sat_desc = conf_dict['sat_desc']
        self.sat.sat_name = conf_dict['sat_name']
        self.sat.update_lifecycle_immediately = conf_dict['update_lifecycle_immediately']
        self.sat.create_new_env = conf_dict['create_new_env']
        self.sat.new_env = conf_dict['new_env']
        self.sat.use_default_org_view = conf_dict['use_default_org_view']
        self.sat.disconnected_mode = conf_dict['disconnected_mode']
        self.sat.rhsm_satellite = conf_dict['rhsm_satellite']


    def __init_cfme(self, conf_dict):
        self.cfme = CFME()
        self.cfme.cfme_address = conf_dict['cfme_address']
        self.cfme.cfme_admin_password = conf_dict['cfme_admin_password']
        self.cfme.cfme_install_loc = conf_dict['cfme_install_loc']
        self.cfme.cfme_root_password = conf_dict['cfme_root_password']
        self.cfme.cfme_db_password = conf_dict['cfme_db_password']

    def __init_osp(self, conf_dict):
        self.osp = OSP()
        self.osp.compute_count = conf_dict['compute_count']
        self.osp.controller_count = conf_dict['controller_count']
        self.osp.block_storage_count = conf_dict['block_storage_count']
        self.osp.object_storage_count = conf_dict['object_storage_count']
        self.osp.director_address = conf_dict['director_address']
        self.osp.director_ui_url = conf_dict['director_ui_url']
        self.osp.director_vm_name = conf_dict['director_vm_name']
        self.osp.overcloud_nodes = conf_dict['overcloud_nodes']
        self.osp.undercloud_address = conf_dict['undercloud_address']
        self.osp.undercloud_pass = conf_dict['undercloud_pass']
        self.osp.undercloud_user = conf_dict['undercloud_user']
        self.osp.network = conf_dict['network']

    def __init_ocp(self, conf_dict):
        self.ocp = OCP()
        self.ocp.ose_address = conf_dict['ose_address']
        self.ocp.subscription = conf_dict['subscription']
        self.ocp.install_loc = conf_dict['install_loc']
        self.ocp.storage_size = conf_dict['storage_size']
        self.ocp.username = conf_dict['username']
        self.ocp.user_password = conf_dict['user_password']
        self.ocp.root_password = conf_dict['root_password']
        self.ocp.master_vcpu = conf_dict['master_vcpu']
        self.ocp.master_ram = conf_dict['master_ram']
        self.ocp.master_disk = conf_dict['master_disk']
        self.ocp.node_vcpu = conf_dict['node_vcpu']
        self.ocp.node_ram = conf_dict['node_ram']
        self.ocp.node_disk = conf_dict['node_disk']
        self.ocp.available_vcpu = conf_dict['available_vcpu']
        self.ocp.available_ram = conf_dict['available_ram']
        self.ocp.available_disk = conf_dict['available_disk']
        self.ocp.number_master_nodes = conf_dict['number_master_nodes']
        self.ocp.number_worker_nodes = conf_dict['number_worker_nodes']
        self.ocp.storage_type = conf_dict['storage_type']
        self.ocp.storage_name = conf_dict['storage_name']
        self.ocp.storage_host = conf_dict['storage_host']
        self.ocp.export_path = conf_dict['export_path']
        self.ocp.subdomain_name = conf_dict['subdomain_name']
        self.ocp.sample_apps = conf_dict['sample_apps']
