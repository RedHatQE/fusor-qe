import yaml


class ProductConfig(object):
    '''
    A simple mapping of dictionary keys to instance attributes
    '''
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


class UIDeploymentRunner(object):
    '''
    This class manages the configuration and workflow for a QCI deployment
    defined by a yaml file.
    '''

    def __init__(self, path='./variables.yaml'):
        with open(path, 'r') as conffile:
            self.conf = yaml.load(conffile)
        self.rhv = ProductConfig(self.conf['deployment']['products']['rhv'])
        self.sat = ProductConfig(self.conf['deployment']['products']['sat'])
        self.cfme = ProductConfig(self.conf['deployment']['products']['cfme'])

        self.products = self.conf['deployment']['install']
        self.deployment_id = self.conf['deployment']['deployment_id']
        self.password = self.conf['credentials']['fusor']['password']

    def product_selection(self, page):
        '''SelectProductsPage'''
        page.select_products(self.products)
        return page.click_next()

    def deployment_name(self, page):
        '''DeploymentName'''
        page.set_name(self.sat.sat_name)
        page.set_description(self.sat.sat_desc)
        page.set_password(self.password)
        page.set_confirm_password(self.password)
        return page.click_next()

    def update_availability(self, page):
        '''UpdateAvailability'''
        if self.sat.update_lifecycle == 'immediately':
            page.click_immediately()
        else:
            # TODO: write workflow for "after_publishing"
            pass
        return page.click_next()

    def access_insights(self, page):
        '''Insights'''
        if self.sat.enable_access_insights:
            page.click_enable()
        return page.click_next()

    def setup_type(self, page):
        '''SetupType '''
        if self.rhv.rhv_setup_type == 'rhevhost':
            page.click_hypervisor_engine()
        elif self.rhv.rhv_setup_type == 'selfhost':
            page.click_self_hosted()
        else:
            raise Exception("{} is not a valid rhv setup \
                            type".format(self.rhv.rhv_setup_type))
        return page.click_next()

    def engine(self, page):
        '''Engine'''
        rhv_host = page.hosts.get_host_by_mac(self.rhv.rhvm_mac)
        rhv_host.choose()
        return page.click_next()

    def hypervisor(self, page):
        '''Hypervisor'''
        # Since WebUI pre-populates the SH engine vm name w/ default value
        # use yaml value if it isn't null
        if self.rhv.rhv_setup_type == 'selfhost' and self.rhv.self_hosted_engine_hostname:
            page.set_engine_hostname(self.rhv.self_hosted_engine_hostname)

        for mac in self.rhv.rhvh_macs:
            rhv_h = page.hosts.get_host_by_mac(mac)
            rhv_h.choose()
        return page.click_next()

    def rhv_configuration(self, page):
        '''Configuration'''
        page.set_root_passwords(self.password)
        page.set_engine_passwords(self.password)

        # Custom data center & cluster name in RHVSH disabled for QCI 1.0
        # See https://bugzilla.redhat.com/show_bug.cgi?id=1367777
        if self.rhv.rhv_setup_type != 'selfhost':
            page.set_data_center_name(self.rhv.data_center_name)
            page.set_cluster_name(self.rhv.cluster_name)

        page.set_cpu_type(self.rhv.cpu_type)
        return page.click_next()

    def rhv_storage(self, page):
        '''RHV Storage'''
        if self.rhv.storage_type == 'NFS':
            page.click_nfs()
        elif self.rhv.storage_type == 'Gluster':
            page.click_gluster()
        else:
            raise Exception("{} is not a valid rhv storage \
                            type".format(self.rhv.storage_type))
        page.set_data_domain_name(self.rhv.data_domain_name)
        page.set_storage_address(self.rhv.data_domain_address)
        page.set_share_path(self.rhv.data_domain_share_path)
        if 'cfme' in self.products:
            page.set_export_domain_name(self.rhv.export_domain_name)
            page.set_export_storage_address(self.rhv.export_domain_address)
            page.set_export_share_path(self.rhv.export_domain_share_path)

        if self.rhv.rhv_setup_type == 'selfhost':
            page.set_hosted_domain_name(self.rhv.selfhosted_domain_name)
            page.set_hosted_storage_address(self.rhv.selfhosted_domain_address)
            page.set_hosted_share_path(self.rhv.selfhosted_domain_share_path)

        return page.click_next()

    def cfme_install(self, page):
        '''CFME Installation Location'''
        if self.cfme.cfme_install_loc == 'rhv':
            page.click_install_on_rhv()
        elif self.cfme.cfme_install_loc == 'osp':
            page.click_install_on_osp()
        else:
            raise Exception("{} is not a valid install location for \
                            CFME".format(self.cfme.cfme_install_loc))
        return page.click_next()

    def cfme_config(self, page):
        '''CFME Configuration'''
        page.set_root_passwords(self.cfme.cfme_root_password)
        page.set_admin_passwords(self.cfme.cfme_admin_password)
        page.set_db_passwords(self.cfme.cfme_db_password)
        return page.click_next()

    def content_provider(self, page):
        '''Content Provider Page'''
        if not self.sat.disconnected_mode:
            page.click_redhat_cdn()
            page.set_username(self.conf['credentials']['cdn']['username'])
            page.set_password(self.conf['credentials']['cdn']['password'])
        else:
            page.click_disconnected()
            page.set_disconnected_url_field(self.sat.disconnected_url)
        return page.click_next()

    def subscription_management(self, page):
        '''Subscription Management Application'''
        page.click_sma_radio_by_uuid(self.sat.rhsm_satellite['uuid'])
        return page.click_next()

    def add_subscriptions(self, page):
        '''Add Subscriptions'''
        return page.click_next()

    def review_subscriptions(self, page):
        '''Review Subscriptions'''
        return page.click_next()

    def installation_review(self, page):
        '''Installation Review'''
        return page.click_deploy()
