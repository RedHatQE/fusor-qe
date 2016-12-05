import yaml
import ipaddress
from selenium.webdriver.common.by import By


class UnknownDriverTypeError(Exception):
    '''
    Exception for unknown host driver type.
    '''
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Unknown driver type: '{}'".format(self.name)


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
        self.osp = ProductConfig(self.conf['deployment']['products']['osp'])
        self.ocp = ProductConfig(self.conf['deployment']['products']['ose'])

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

    def osp_detect_undercloud(self, page):
        '''OSP Detect Undercloud Page filler'''
        # First we wait on the spinner that appears.   It says:
        #
        #   Inspecting Undercloud
        page.wait_on_spinner(timeout=300)

        page.set_undercloud_ip(self.osp.undercloud_address)
        page.set_ssh_user(self.osp.undercloud_user)
        page.set_ssh_password(self.osp.undercloud_pass)
        page.click_detect_undercloud()
        return page.click_next()

    def osp_register_nodes(self, page):
        '''
        OSP Register Nodes Page Filler

        This one is pretty complicated.   First we have to click register
        nodes button.   This opens a modal, where one can fill in various ways
        of selecting our nodes.   Presently, we only support doing autodetect.
        Information to do autodetec is filled in and then Next is selected, but
        this takes you to a new modal where you select which machines to
        register.

        TODO: The yaml and software supports registering nodes from multiple
              Hosts, however this code only supports one Host presently.
              At some point we should make it support multiple hosts.
        '''
        # First we wait on the spinner that appears.   It says:
        #
        #   Loading OSP Nodes
        page.wait_on_spinner(timeout=300)

        ##################################
        # The Register Nodes Modal Frame #
        ##################################
        for node_registration_info in self.osp.overcloud_nodes:
            page.click_register_nodes()
            self._osp_determine_how_to_register_nodes(
                page,
                node_registration_info
            )

        # Wait for the spinners to be done.   So after you start a node
        # to be registered, it doesn't show up for a bit, and then it shows
        # up but with a ! in a triangle.   Finally this transitions to a
        # progress bar.   So we wait through the three transitions:
        #
        #   - Wait for exclamation triangle to appear
        #   - Wait for exclamation triangle to disappear
        #   - Wait for progress bar to go away.
        #
        # XXX:   Maybe this should go in the page object itself.
        exclamation_triangle_loc = (
            By.XPATH,
            "//span[contains(@class, 'fa-exclamation-triangle')]"
        )
        page.wait_until_element_is_visible(
            locator=exclamation_triangle_loc,
            timeout=300,
        )
        page.wait_until_element_is_not_visible(
            locator=exclamation_triangle_loc,
            timeout=300,
        )
        page.wait_on_spinner(
            timeout=360,
            spin_class='spinner-xs',
        )

        return page.click_next()

    def _osp_determine_how_to_register_nodes(self, page, node_registration_info):
        '''
        Handles filling out information for the:

            Determine How to Register Nodes:

        Modal frame that is part of the RHOSP:Register Nodes Page.
        '''
        host_ip = node_registration_info['host_ip']
        driver_type = node_registration_info['driver_type']
        host_username = node_registration_info['host_username']
        host_password = node_registration_info['host_password']
        mac_address = node_registration_info['mac_address']

        # Click on "autodect or specify nodes" so we can fill the form out
        # to manually specify the nodes.
        # TODO: Need to add support for CSV file.
        # TODO: Need to add support for autodetection.
        if not page.autodetect_or_specify.is_selected:
            page.click_autodetect_or_specify()

        # Fill in all the information up to the autodetect slider.
        page.set_ip_address(host_ip)
        drivers_selector = page.driver
        drivers_selector.select_by_value(driver_type)
        page.set_username(host_username)
        page.set_password(host_password)

        #
        # TODO: Need to add autodetect deselection back.
        # See:
        #
        #   https://github.com/RedHatQE/fusor-qe/pull/70#discussion_r90135582

        # TODO: When we support autodetect add this back.   It worked, and its
        #       going back so I'm not deleting it, and just commenting it out.
        #        # Handle the vendor select widget
        #        if driver_type == 'pxe_ssh':
        #            vendor_selector = page.ssh_vendor
        #        elif driver_type == 'pxe_ipmitool':
        #            vendor_selector = page.ipmi_vendor
        #        else:
        #            raise UnknownDriverTypeError(driver_type)
        #
        #        vendor_selector.select_by_value(vendor)

        # Send the mac address:
        page.set_mac_addresses(mac_address)

        # Register the node:
        page.click_register()

    def osp_assign_nodes(self, page):
        roles = (
            {
                'name': 'compute',
                'nodes': self.osp.compute_count,
                'assign_func': lambda page: page.click_compute_list(),
            },
            {
                'name': 'controller',
                'nodes': self.osp.controller_count,
                'assign_func': lambda page: page.click_controller_list(),
            },
            {
                'name': 'block_storage',
                'nodes': self.osp.block_storage_count,
                'assign_func': lambda page: page.click_block_storage_list(),
            },
            {
                'name': 'object_storage',
                'nodes': self.osp.object_storage_count,
                'assign_func': lambda page: page.click_object_storage_list(),
            },
        )

        # First we wait on a spinner that says:
        #
        #   Loading...
        page.wait_on_spinner(timeout=300)

        #
        # Iterate across the roles and assign the ones that have a node
        # count.
        for role in roles:
            role_name = role['name']
            role_node_count = role['nodes']
            role_assign_func = role['assign_func']

            if role_node_count == 0:
                continue

            # Assign the role
            page.click_assign_role()
            role_assign_func(page)

            # Set the number of nodes if need be:
            cur_count = page.get_selector_assigned_role_node_count(role_name)
            if cur_count != role_node_count:
                page.select_assigned_role_node_count(role_name, role_node_count)

        return page.click_next()

    def osp_configure_overcloud(self, page):
        # TODO: Support Ceph Storage
        external_interface = self.osp.network['external_interface']
        private_network_addr = self.osp.network['provision_network']['network']
        private_network_mask = self.osp.network['provision_network']['subnet']
        floating_ip_network_addr = self.osp.network['public_network']['network']
        floating_ip_network_mask = self.osp.network['public_network']['subnet']
        floating_ip_network_gateway = self.osp.network['public_network']['gateway']
        admin_password = self.osp.undercloud_pass

        # Get the network addresses into an IPv4Network object so
        # we can easily and consistently produce a CIDR format.
        private_network = ipaddress.ip_network(
            unicode(
                "{}/{}".format(
                    private_network_addr,
                    private_network_mask
                )
            )
        )
        floating_ip_network = ipaddress.ip_network(
            unicode(
                "{}/{}".format(
                    floating_ip_network_addr,
                    floating_ip_network_mask
                )
            )
        )

        # Set items on configuration page:
        page.set_external_net_interface(external_interface)
        page.set_private_net(private_network.exploded)
        page.set_floating_ip_net(floating_ip_network.exploded)
        page.set_floating_ip_net_gateway(floating_ip_network_gateway)
        page.set_admin_passwords(admin_password)

    def ocp_nodes(self, page):
        '''
        OpenShift Master/Nodes specs
        NOTE: Does not automate the input of custom node details
        '''
        if self.ocp.install_loc == 'rhv':
            page.click_rhv()
        else:
            raise Exception("QCI install of OpenShift only support on RHV")

        page.click_worker_nodes(self.ocp.number_worker_nodes)
        page.click_additional_storage(self.ocp.node_disk)

        return page.click_next()

    def ocp_configuration(self, page):
        '''
        OpenShift Configuration
        '''

        if self.ocp.storage_type == 'gluster':
            page.click_gluster_radio()
        elif self.ocp.storage_type == 'NFS':
            page.click_nfs_radio()
        else:
            raise Exception('Invalid storage type for OpenShift: {}'.format(
                self.ocp.storage_type))

        page.set_host(self.ocp.storage_host)
        page.set_export_path(self.ocp.export_path)
        page.set_username(self.ocp.username)
        page.set_password(self.ocp.user_password)
        page.set_confirm_password(self.ocp.user_password)
        page.set_subdomain(self.ocp.subdomain_name)

        if 'openshift_hello_world' in self.ocp.sample_apps:
            page.click_hello_world()

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
