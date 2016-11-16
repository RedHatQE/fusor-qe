# XXX: Every one of the roles has an edit modal frame.   Each edit
#      frame has  Overall Settings and Service Configuration tabs.
#      Each of these tabs has many input fields of various sorts.
#      None of this has been implemented in this library yet.
#
#      See https://projects.engineering.redhat.com/browse/RHCIQE-239

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from pages.qci_page import QCIPage


# Huge map of Global Config input field names to their type.
# Their type can be either "text" or "checkbox".   Number types
# are just treated as text.
#
# Why do we do this?   There are over 200 input fields for the
# Global Config, so instead of creating individual locators,
# properties and set and click functions we just have the
# following functions:
#
#   global_config_element_locator(self, name) - generates the locator
#   global_config_element(self, name)         - returns the element
#   set_global_config(self, name, value)      - sets an input field.
#   click_global_config(self, name, value)    - clicks an input field.
global_config_to_type_map = {
    'AdminPassword': 'text',
    'AdminToken': 'text',
    'CeilometerBackend': 'text',
    'CeilometerComputeAgent': 'text',
    'CeilometerMeteringSecret': 'text',
    'CeilometerPassword': 'text',
    'CephAdminKey': 'text',
    'CephClientKey': 'text',
    'CephClusterFSID': 'text',
    'CephExternalMonHost': 'text',
    'CephMonKey': 'text',
    'CephStorageCount': 'text',
    'CephStorageHostnameFormat': 'text',
    'CephStorageImage': 'text',
    'CloudDomain': 'text',
    'CloudName': 'text',
    'CorosyncIPv6': 'checkbox',
    'Debug': 'text',
    'DeployIdentifier': 'text',
    'EnableFencing': 'checkbox',
    'EnableGalera': 'checkbox',
    'GlanceBackend': 'text',
    'GlanceLogFile': 'text',
    'GlanceNotifierStrategy': 'text',
    'GlancePassword': 'text',
    'HAProxySyslogAddress': 'text',
    'HeatPassword': 'text',
    'HeatStackDomainAdminPassword': 'text',
    'HorizonAllowedHosts': 'text',
    'HypervisorNeutronPhysicalBridge': 'text',
    'HypervisorNeutronPublicInterface': 'text',
    'ImageUpdatePolicy': 'text',
    'InstanceNameTemplate': 'text',
    'KeyName': 'text',
    'KeystoneCACertificate': 'text',
    'KeystoneNotificationDriver': 'text',
    'KeystoneNotificationFormat': 'text',
    'KeystoneSSLCertificate': 'text',
    'KeystoneSSLCertificateKey': 'text',
    'KeystoneSigningCertificate': 'text',
    'KeystoneSigningKey': 'text',
    'ManageFirewall': 'checkbox',
    'MemcachedIPv6': 'checkbox',
    'MongoDbIPv6': 'checkbox',
    'MongoDbNoJournal': 'checkbox',
    'MysqlInnodbBufferPoolSize': 'text',
    'MysqlMaxConnections': 'text',
    'NeutronAgentExtensions': 'text',
    'NeutronAgentMode': 'text',
    'NeutronAllowL3AgentFailover': 'text',
    'NeutronBridgeMappings': 'text',
    'NeutronComputeAgentMode': 'text',
    'NeutronControlPlaneID': 'text',
    'NeutronCorePlugin': 'text',
    'NeutronDVR': 'text',
    'NeutronDhcpAgentsPerNetwork': 'text',
    'NeutronDnsmasqOptions': 'text',
    'NeutronEnableIsolatedMetadata': 'text',
    'NeutronEnableL2Pop': 'text',
    'NeutronEnableTunnelling': 'text',
    'NeutronExternalNetworkBridge': 'text',
    'NeutronFlatNetworks': 'text',
    'NeutronL3HA': 'text',
    'NeutronMechanismDrivers': 'text',
    'NeutronMetadataProxySharedSecret': 'text',
    'NeutronNetworkType': 'text',
    'NeutronNetworkVLANRanges': 'text',
    'NeutronPassword': 'text',
    'NeutronPluginExtensions': 'text',
    'NeutronPublicInterface': 'text',
    'NeutronPublicInterfaceDefaultRoute': 'text',
    'NeutronPublicInterfaceIP': 'text',
    'NeutronPublicInterfaceRawDevice': 'text',
    'NeutronPublicInterfaceTag': 'text',
    'NeutronServicePlugins': 'text',
    'NeutronTenantMtu': 'text',
    'NeutronTunnelIdRanges': 'text',
    'NeutronTunnelTypes': 'text',
    'NeutronTypeDrivers': 'text',
    'NeutronVniRanges': 'text',
    'NtpServer': 'text',
    'OvercloudCephStorageFlavor': 'text',
    'PublicVirtualInterface': 'text',
    'PurgeFirewallRules': 'checkbox',
    'RabbitClientPort': 'text',
    'RabbitClientUseSSL': 'text',
    'RabbitCookieSalt': 'text',
    'RabbitFDLimit': 'text',
    'RabbitIPv6': 'checkbox',
    'RabbitPassword': 'text',
    'RabbitUserName': 'text',
    'RedisPassword': 'text',
    'SnmpdReadonlyUserName': 'text',
    'SnmpdReadonlyUserPassword': 'text',
    'TimeZone': 'text',
    'UpdateIdentifier': 'text',
    'PingTestIps': 'text',
    'ConfigDebug': 'checkbox',
    'DeployArtifactURLs': 'text',
    'CephClientUserName': 'text',
    'CephIPv6': 'checkbox',
    'GlanceRbdPoolName': 'text',
    'ceph_admin_key': 'text',
    'ceph_client_key': 'text',
    'ceph_external_mon_ips': 'text',
    'ceph_fsid': 'text',
    'ceph_mon_ips': 'text',
    'ceph_mon_key': 'text',
    'ceph_mon_names': 'text',
    'ceph_storage_count': 'text',
    'EnablePackageInstall': 'checkbox',
    'Flavor': 'text',
    'GlanceHost': 'text',
    'Hostname': 'text',
    'Image': 'text',
    'KeystoneAdminApiVirtualIP': 'text',
    'KeystonePublicApiVirtualIP': 'text',
    'NetworkDeploymentActions': 'text',
    'NeutronHost': 'text',
    'NeutronPhysicalBridge': 'text',
    'NodeIndex': 'text',
    'RabbitHost': 'text',
    'SoftwareConfigTransport': 'text',
    'UpgradeLevelNovaCompute': 'text',
    'server': 'text',
    'NetworkName': 'text',
    'PortName': 'text',
    'ServiceName': 'text',
    'ExternalIp': 'text',
    'ExternalIpUri': 'text',
    'InternalApiIp': 'text',
    'InternalApiIpUri': 'text',
    'ManagementIp': 'text',
    'ManagementIpUri': 'text',
    'StorageIp': 'text',
    'StorageIpUri': 'text',
    'StorageMgmtIp': 'text',
    'StorageMgmtIpUri': 'text',
    'TenantIp': 'text',
    'TenantIpUri': 'text',
    'ExternalIpSubnet': 'text',
    'InternalApiIpSubnet': 'text',
    'ManagementIpSubnet': 'text',
    'StorageIpSubnet': 'text',
    'StorageMgmtIpSubnet': 'text',
    'TenantIpSubnet': 'text',
    'node_admin_username': 'text',
    'CeilometerApiVirtualIP': 'text',
    'CeilometerStoreEvents': 'checkbox',
    'CeilometerWorkers': 'text',
    'EnableCephStorage': 'checkbox',
    'EnableLoadBalancer': 'checkbox',
    'EnableSwiftStorage': 'checkbox',
    'GlanceApiVirtualIP': 'text',
    'GlanceFilePcmkDevice': 'text',
    'GlanceFilePcmkFstype': 'text',
    'GlanceFilePcmkManage': 'checkbox',
    'GlanceFilePcmkOptions': 'text',
    'GlanceRegistryVirtualIP': 'text',
    'GlanceWorkers': 'text',
    'HAProxyStatsPassword': 'text',
    'HAProxyStatsUser': 'text',
    'HeatApiVirtualIP': 'text',
    'HeatApiVirtualIPUri': 'text',
    'HeatAuthEncryptionKey': 'text',
    'HeatEnableDBPurge': 'checkbox',
    'HeatWorkers': 'text',
    'HorizonSecret': 'text',
    'KeystoneEnableDBPurge': 'checkbox',
    'KeystoneWorkers': 'text',
    'MysqlClusterUniquePart': 'text',
    'MysqlRootPassword': 'text',
    'MysqlVirtualIP': 'text',
    'MysqlVirtualIPUri': 'text',
    'NeutronApiVirtualIP': 'text',
    'NeutronEnableDHCPAgent': 'checkbox',
    'NeutronEnableL3Agent': 'checkbox',
    'NeutronEnableMetadataAgent': 'checkbox',
    'NeutronEnableOVSAgent': 'checkbox',
    'NeutronWorkers': 'text',
    'PcsdPassword': 'text',
    'PublicVirtualIP': 'text',
    'RabbitCookie': 'text',
    'RedisVirtualIP': 'text',
    'RedisVirtualIPUri': 'text',
    'VirtualIP': 'text',
    'DeployedSSLCertificatePath': 'text',
    'bootstrap_nodeid': 'text',
    'bootstrap_nodeid_ip': 'text',
    'ExternalIpList': 'text',
    'InternalApiIpList': 'text',
    'ManagementIpList': 'text',
    'StorageIpList': 'text',
    'StorageMgmtIpList': 'text',
    'TenantIpList': 'text',
    'controller_swift_devices': 'text',
    'controller_swift_proxy_memcaches': 'text',
    'object_store_swift_devices': 'text',
    'block_storage_hosts': 'text',
    'ceilometer_api_node_ips': 'text',
    'ceph_storage_hosts': 'text',
    'cinder_api_node_ips': 'text',
    'compute_hosts': 'text',
    'controller_hosts': 'text',
    'controller_ips': 'text',
    'controller_names': 'text',
    'glance_api_node_ips': 'text',
    'glance_registry_node_ips': 'text',
    'heat_api_node_ips': 'text',
    'horizon_node_ips': 'text',
    'keystone_admin_api_node_ips': 'text',
    'keystone_public_api_node_ips': 'text',
    'memcache_node_ips': 'text',
    'mongo_node_ips': 'text',
    'mysql_node_ips': 'text',
    'neutron_api_node_ips': 'text',
    'nova_api_node_ips': 'text',
    'nova_metadata_node_ips': 'text',
    'object_storage_hosts': 'text',
    'rabbit_node_ips': 'text',
    'redis_node_ips': 'text',
    'swift_proxy_node_ips': 'text',
}

role_to_box_name = {
    'compute': 'Compute',
    'controller': 'Controller',
    'block-storage': 'Block Storage',
    'object-storage': 'Object Storage',
}


class GlobalConfItemUndefinedError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Undefined global config item: {}".format(self.name)


class GlobalConfItemTypeError(Exception):
    def __init__(self, name, needed_type, cur_type):
        self.name = name
        self.needed_type = needed_type
        self.cur_type = cur_type

    def __str__(self):
        return "Global config item {} needed type {} provided type {}".format(
            self.name,
            self.needed_type,
            self.cur_type,
        )


class AssignNodes(QCIPage):
    _page_title = "QuickStart Cloud Installer"

    # * locators *
    # <<< MAIN Page >>>
    _edit_global_config_loc = (
        By.XPATH,
        "//a[@class  = 'edit-global-config']"
    )
    _assign_role_loc = (
        By.XPATH,
        "//a[contains(.,'Assign Role')]",
    )
    _assign_role_draggable_target_loc = (
        By.XPATH,
        "//ul[contains(@class, 'deployment-roles-assigned')]//div[contains(@class, 'draggable-object-target')]",
    )

    # We have the different roles listed twice.   Up top
    # in little boxes they are there to be drug and dropped on
    # assign role.   If however you click on assign role they drop
    # down as a list (technically still in a box, but).   So we
    # name the ones up top with _box_loc appended to their names,
    # the ones in the dropdown with _list_loc appended to their names.
    _role_box_template_loc = (
        By.XPATH,
        "//div[@data-qci = '{}']",
    )
    _compute_list_loc = (
        By.XPATH,
        "//a[contains(@class, 'roles-menu-item') and contains(., 'Compute')]",
    )
    _controller_list_loc = (
        By.XPATH,
        "//a[contains(@class, 'roles-menu-item') and contains(., 'Controller')]",
    )
    _block_storage_list_loc = (
        By.XPATH,
        "//a[contains(@class, 'roles-menu-item') and contains(., 'BlockStorage')]",
    )
    _object_storage_list_loc = (
        By.XPATH,
        "//a[contains(@class, 'roles-menu-item') and contains(., 'ObjectStorage')]",
    )
    # Once a role is selected it becomes a list element
    # with a class element containing 'role-$role'.  Each of these
    # list elements contain three controls:
    #
    #   - delete
    #   - edit
    #   - node count
    _assigned_role_template_loc = (
        By.XPATH,
        "//li[contains(@class, 'role-{}')]",
    )
    _assigned_role_delete_template_loc = (
        By.XPATH,
        "{}/a[@data-qci = 'removeRole']".format(
            _assigned_role_template_loc[1]
        ),
    )
    _assigned_role_edit_template_loc = (
        By.XPATH,
        "{}/a[@data-qci = 'editRole']".format(
            _assigned_role_template_loc[1]
        ),
    )
    _assigned_role_node_count_template_loc = (
        By.XPATH,
        "{}/select".format(
            _assigned_role_template_loc[1]
        ),
    )

    # <<< Edit Global Config >>>
    _global_config_cancel_loc = (
        By.XPATH,
        "//button[@data-qci = 'cancel-edit-global-config']"
    )
    _global_config_save_loc = (
        By.XPATH,
        "//button[@data-qci = 'save-edit-global-config']"
    )

    # **************
    # * properties *
    # **************
    @property
    def edit_global_config(self):
        return self.selenium.find_element(*self._edit_global_config_loc)

    @property
    def assign_role(self):
        return self.selenium.find_element(*self._assign_role_loc)

    @property
    def assign_role_draggable_target(self):
        return self.selenium.find_element(
            *self._assign_role_draggable_target_loc
        )

    @property
    def compute_box(self):
        return self.selenium.find_element(*self._compute_box_loc)

    @property
    def controller_box(self):
        return self.selenium.find_element(*self._compute_box_loc)

    @property
    def block_storage_box(self):
        return self.selenium.find_element(*self._compute_box_loc)

    @property
    def object_storage_box(self):
        return self.selenium.find_element(*self._compute_box_loc)

    @property
    def compute_list(self):
        return self.selenium.find_element(*self._compute_list_loc)

    @property
    def controller_list(self):
        return self.selenium.find_element(*self._controller_list_loc)

    @property
    def block_storage_list(self):
        return self.selenium.find_element(*self._block_storage_list_loc)

    @property
    def object_storage_list(self):
        return self.selenium.find_element(*self._object_storage_list_loc)

    # <<< Edit Global Config >>>
    @property
    def global_config_cancel(self):
        return self.selenium.find_element(*self._global_config_cancel_loc)

    @property
    def global_config_save(self):
        return self.selenium.find_element(*self._global_config_save_loc)

    # actions
    # <<< Main Page >>>
    def click_edit_global_config(self):
        self.edit_global_config.click()

    def click_assign_role(self):
        self.assign_role.click()

    def click_compute_list(self):
        self.compute_list.click()

    def click_controller_list(self):
        self.controller_list.click()

    def click_block_storage_list(self):
        self.block_storage_list.click()

    def click_object_storage_list(self):
        self.object_storage_list.click()

    # role for these functions can be:
    #
    #   - controller
    #   - compute
    #   - block-storage
    #   - object-storage
    def get_role_box(self, role):
        locator_type = self._role_box_template_loc[0]
        locator = self._role_box_template_loc[1].format(role)
        return self.selenium.find_element(locator_type, locator)

    def get_selector_assigned_role_node_count(self, role):
        locator_type = self._assigned_role_node_count_template_loc[0]
        locator = self._assigned_role_node_count_template_loc[1].format(role)
        return Select(self.selenium.find_element(locator_type, locator))

    def get_assigned_role_node_count_options(self, role):
        selector = self.get_selector_assigned_role_node_count(role)
        node_choices = []
        for option in selector.options():
            node_choices.append(option.get_attribute('value'))
        return node_choices

    def hover_assigned_role(self, role):
        locator_type = self._assigned_role_template_loc[0]
        locator = self._assigned_role_template_loc[1].format(role)
        hover_element = self.selenium.find_element(locator_type, locator)
        hover = ActionChains(self.selenium).move_to_element(hover_element)
        hover.perform()

    def select_assigned_role_node_count(self, role, count):
        selector = self.get_selector_assigned_role_node_count(role)
        selector.select_by_value("{}".format(count))

    def click_assigned_role_edit(self, role):
        # Have to give assigned role focus before the
        # delete button becomes accessible.
        self.hover_assigned_role(role)

        locator_type = self._assigned_role_edit_template_loc[0]
        locator = self._assigned_role_edit_template_loc[1].format(role)
        self.selenium.find_element(locator_type, locator).click()

    def click_assigned_role_delete(self, role):
        # Have to give assigned role focus before the
        # delete button becomes accessible.
        self.hover_assigned_role(role)

        # Now we can click it.
        locator_type = self._assigned_role_delete_template_loc[0]
        locator = self._assigned_role_delete_template_loc[1].format(role)
        self.selenium.find_element(locator_type, locator).click()

    # XXX:  Presently this does not work.   It selects the source
    #       but never places it on the target.   I don't understand why
    #       thought perhaps it was that we had the source and target
    #       locators wrong, but if that is so we never found the correct
    #       combination.   At this point the locators are set the way
    #       development suggested.
    def assign_role_by_drag(self, role):
        role_box_source = self.get_role_box(role)
        assign_role_target = self.assign_role_draggable_target
        actions = ActionChains(self.selenium)
        actions.drag_and_drop(role_box_source, assign_role_target).perform()

    #
    # <<< Edit Global Config >>>
    def global_config_element_locator(self, name):
        if not(name in global_config_to_type_map):
            raise GlobalConfItemUndefinedError(name)

        locator = (By.XPATH, "//input[@id = '{}']".format(name))
        return locator

    def global_config_element(self, name):
        locator = self.global_config_element_locator(name)
        return self.selenium.find_element(*locator)

    def set_global_config(self, name, value):
        element = self.global_config_element(name)
        if global_config_to_type_map[name] == 'checkbox':
            raise GlobalConfItemTypeError(
                name=name,
                needed_type='text',
                cur_type='checkbox',
            )

        element.clear()
        element.send_keys(value)

    def click_global_config(self, name):
        element = self.global_config_element(name)
        element.click()

    def set_undercloud_ip(self, text):
        self.undercloud_ip.clear()
        self.undercloud_ip.send_keys(text)

    def click_global_config_cancel(self):
        self.global_config_cancel.click()

    def click_global_config_save(self):
        self.global_config_save.click()
