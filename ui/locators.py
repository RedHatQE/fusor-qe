# -*- encoding: utf-8 -*-
"""Implements different locators for UI"""

import collections
import logging

from selenium.webdriver.common.by import By


LOGGER = logging.getLogger(__name__)


class LocatorDict(collections.Mapping):
    """This class will log every time an item is selected

    The constructor accepts a dictionary or keyword arguments like the
    built-in ``dict``::

        >>> dict({'a': 'b'})
        {'a': 'b'}
        >>> dict(a='b')
        {'a': 'b'}

    """
    def __init__(self, *args, **kwargs):
        self.store = dict(*args, **kwargs)

    def __getitem__(self, key):
        item = self.store[key]
        LOGGER.debug(
            'Accessing locator "%s" by %s: "%s"', key, item[0], item[1]
        )
        return item

    def __len__(self):
        return len(self.store)

    def __iter__(self):
        return iter(self.store)


locators = LocatorDict({
    # RHCI
    "rhci.new": (
        By.XPATH, "//a[contains(.,'New Deployment')]"),
    "rhci.product_select": (
        By.XPATH, "//span[contains(@id,'%s')]/div[contains(@class, 'rhci-footer-unselected')]"),
    "rhci.product_deselect": (
        By.XPATH, "//span[contains(@id,'%s')]/div[contains(@class, 'rhci-footer-selected')]"),
    "rhci.next": (
        By.XPATH, "(//a|//button)[contains(.,'Next') and contains(@class, 'btn-primary') and not(contains(@class, 'disabled'))]"),
    "rhci.select": (
        By.XPATH, "//a[contains(.,'Select') and contains(@class, 'btn-primary') and not(contains(@class, 'disabled'))]"),
    "rhci.satellite_name": (
        By.XPATH, "//input[@id='deployment_new_sat_name']"),
    "rhci.satellite_description": (
        By.XPATH, "//textarea[@id='deployment_new_sat_desc']"),
    "rhci.deployment_org": (
        By.XPATH, "//input[@name='deployment-organization']"),
    "rhci.use_default_org_view": (
        By.XPATH, "//input[@name='useDefaultOrgViewForEnv']"),
    "rhci.update_lifecycle_select": (
        By.XPATH, "//input[@value='%s']"),
    "rhci.active_view": (By.XPATH, "//li[contains(@class,'ember-view active')]/a[contains(.,'%s')]"),
    "rhci.env_path": (
        By.XPATH, "//div[@class='path-selector']//span[contains(.,'%s')]"),
    "rhci.enable_access_insights": (By.XPATH, "//input[@name='enable_access_insights']"),
    "rhci.undercloud_ip": (By.XPATH, "//label[contains(.,'Undercloud IP')]/../div/input"),
    "rhci.undercloud_ssh_user": (By.XPATH, "//label[contains(.,'SSH User')]/../div/input"),
    "rhci.undercloud_ssh_pass": (By.XPATH, "//label[contains(.,'SSH Password')]/../div/input"),
    "rhci.detect_undercloud": (By.XPATH, "//button[contains(.,'Detect Undercloud')]"),
    "rhci.register_nodes": (By.XPATH, "//button[contains(.,'Register Nodes')]"),
    "rhci.node_driver_select":  (By.XPATH, "//label/label[contains(.,'Driver')]/../../div/select"),
    "rhci.node_driver_dropdown_item": (By.XPATH, "//div/select/option[contains(@value, '%s')]"),
    "rhci.node_ip_address": (By.XPATH, "//label/label[contains(.,'Address')]/../../div/input"),
    "rhci.node_ipmi_user": (By.XPATH, "//label/label[contains(.,'User')]/../../div/input"),
    "rhci.node_ipmi_pass": (By.XPATH, "//label/label[contains(.,'Password')]/../../div/input"),
    "rhci.node_nic_mac_address": (By.XPATH, "//input[@id='newNodeManualMacAddressAddInput%s']"),
    "rhci.node_register_nodes": (
        By.XPATH, "//div[contains(@class, 'modal-footer')]/button[contains(.,'Register Nodes')]"),
    "rhci.register_node_count": (By.XPATH, "//a[contains(@class,'nodes-add-button') and contains(@title, 'Add node')]"),
    "rhci.node_add_node": (By.XPATH, "//a[contains(@class,'nodes-add-button') and contains(@title, 'Add node')]"),
    "rhci.node_add_node_manual": (By.XPATH, "//button[(@id='manualAddMacAddressButton')]"),
    "rhci.node_register_manual": (By.XPATH, "//input[@type='radio' and contains(@value, 'manual')]"),
    "rhci.node_node_register_submit": (By.XPATH, "//button[@id='newNodeSubmitButton']"),
    "rhci.node_assign_role": (By.XPATH, "//a[@id='role-target-dropdown-1']"),
    "rhci.node_flavor": (By.XPATH, "//div[contains(@class, 'panel') and contains(@class, 'node-profile')]"),
    "rhci.node_manager_panel": (By.XPATH, "//div[contains(@class, 'panel') and contains(@class, 'osp-node-manager-panel')]"),
    "rhci.node_flavor_count": (By.XPATH, "//h4[contains(@class, 'node-profile-free-nodes') and contains(., '%s')]"),
    "rhci.registered_node_count": (By.XPATH, "//span[contains(@class, 'registered-node-count') and contains(., '%s')]"),
    "rhci.node_role_ceph": (By.XPATH, "//a[contains(@class,'role-ceph')]"),
    "rhci.node_role_cinder": (By.XPATH, "//a[contains(@class,'role-cinder')]"),
    "rhci.node_role_controller": (By.XPATH, "//a[contains(@class,'role-controller')]"),
    "rhci.node_role_controller_count_select": (By.XPATH, "//li[contains(@class, 'role-controller') and contains(@class, 'role-assigned')]/select"),
    "rhci.node_role_controller_dropdown_item": (By.XPATH, "//li[contains(@class, 'role-controller') and contains(@class, 'role-assigned')]/select/option[. = '%s']"),
    "rhci.node_role_compute": (By.XPATH, "//a[contains(@class,'role-compute')]"),
    "rhci.node_role_compute_count_select": (By.XPATH, "//li[contains(@class, 'role-compute') and contains(@class, 'role-assigned')]/select"),
    "rhci.node_role_compute_dropdown_item": (By.XPATH, "//li[contains(@class, 'role-compute') and contains(@class, 'role-assigned')]/select/option[. = '%s']"),
    "rhci.node_role_swift": (By.XPATH, "//a[contains(@class,'role-swift')]"),
    "rhci.osp_external_interface": (By.XPATH, "//input[@id='external-osp-interface']"),
    "rhci.osp_private_network": (By.XPATH, "//input[@id='osp-private-network']"),
    "rhci.osp_public_network": (By.XPATH, "//input[@id='osp-floating-network']"),
    "rhci.osp_public_gateway": (By.XPATH, "//input[@id='osp-float-gatewway']"),
    "rhci.osp_overcloud_pass": (By.XPATH, "//input[@id='osp_overcloud_password']"),
    "rhci.osp_overcloud_pass_confirm": (By.XPATH, "//input[@id='confirm_osp_overcloud_password']"),
    "rhci.rhev_setup_type": (
        By.XPATH, "//input[@value='%s']"),
    "rhci.hypervisor_mac_check": (
        By.XPATH, "//td[contains(.,'%s')]/../td/input"),
    "rhci.rhevtab_engine": (
        By.XPATH,
        ("//ul[contains(@class,'nav-pills')]"
         "//a[contains(.,'2B. Engine')]")),
    "rhci.rhevtab_configuration": (
        By.XPATH,
        ("//ul[contains(@class,'nav-pills')]"
         "//a[contains(.,'2C. Configuration')]")),
    "rhci.rhevtab_storage": (
        By.XPATH,
        ("//ul[contains(@class,'nav-pills')]"
         "//a[contains(.,'2D. Storage')]")),
    "rhci.engine_mac_radio": (
        By.XPATH, "//td[contains(.,'%s')]/../td/input"),
    "rhci.rhev_root_pass": (
        By.XPATH, "//input[@id='rhev_root_password' or @id='rhev-root-password']"),
    "rhci.confirm_rhev_root_pass": (
        By.XPATH, "//input[@id='confirm-rhev-root-password']"),
    "rhci.rhevm_adminpass": (
        By.XPATH, "//input[@id='rhev_engine_admin_password' or @id='rhev-engine-admin-password']"),
    "rhci.confirm_rhevm_adminpass": (
        By.XPATH, "//input[@id='confirm-rhev-engine-pdmin-password']"),
    # TODO: File BZ (datacenter != database)
    "rhci.datacenter_name": (
        By.XPATH, "//input[@id='rhev_database_name']"),
    "rhci.cluster_name": (
        By.XPATH, "//input[@id='rhev_cluster_name']"),
    "rhci.cpu_type": (
        By.XPATH,
        ("//div[@class='form-group']/label[contains(.,'CPU Type')]"
         "/following-sibling::div/input")),
    "rhci.storage_type": (
        By.XPATH,
        "//input[@type='radio' and contains(@value, '%s')]"),
    "rhci.data_domain_name": (
        By.XPATH, "//input[@id='rhev_storage_name']"),
    "rhci.export_domain_name": (
        By.XPATH, "//input[@id='rhev_export_domain_name']"),
    "rhci.data_domain_address": (
        By.XPATH, "//input[@id='rhev_storage_address']"),
    "rhci.export_domain_address": (
        By.XPATH, "//input[@id='rhev_export_domain_address']"),
    "rhci.data_domain_share_path": (
        By.XPATH, "//input[@id='rhev_share_path']"),
    "rhci.export_domain_share_path": (
        By.XPATH, "//input[@id='rhev_export_domain_path']"),
    "rhci.bc_cloudforms": (
        By.XPATH,
        "//div[@class='wizard-block']//li[contains(.,'CloudForms')]/div"),
    "rhci.bc_subscriptions": (
        By.XPATH,
        "//div[@class='wizard-block']//li[contains(.,'Subscriptions')]/div"),
    "rhci.cfme_install_on": (
        By.XPATH, "//input[@type='radio' and @value='%s']"),
    "rhci.cfme_admin_password": (
        By.XPATH, "//input[@id='cfme_admin_password']"),
    "rhci.confirm_cfme_admin_password": (
        By.XPATH, "//input[@id='confirm_cfme_admin_password']"),
    "rhci.cfme_root_password": (
        By.XPATH, "//input[@id='cfme_root_password']"),
    "rhci.confirm_cfme_root_password": (
        By.XPATH, "//input[@id='confirm_cfme_root_password']"),
    # TODO: File BZ, these rhsm inputs need IDs.
    "rhci.rhsm_username": (
        By.XPATH,
        ("//div[contains(@class,'form-group')]/label[contains(.,'Red Hat login')]"
        "/following-sibling::div/input")),
    "rhci.rhsm_password": (
        By.XPATH,
        ("//div[contains(@class,'form-group')]/label[contains(.,'Password')]"
        "/following-sibling::div/input")),
    "rhci.rhsm_satellite_radio": (
        By.XPATH, "//input[@type='radio' and contains(@value, '%s')]"),
    "rhci.subscription_check": (
        By.XPATH, "//td[contains(.,'%s')]/../td/input"),
    "rhci.subscription_attach": (
        By.XPATH, "//button[contains(.,'Attach Selected')]"),
    "rhci.deploy": (
        By.XPATH, "//button[contains(.,'Deploy')]"),
    "rhci.rhsm_mirror": (
        By.XPATH,
        ("//div[contains(@class,'form-group')]/label[contains(.,'Content Mirror URL')]"
        "/following-sibling::div/input")),
    "rhci.rhsm_disconnected": (
        By.XPATH,
        "//input[@type='radio' and contains(@value, 'disconnected')]"),
    "rhci.manifest_upload_file": (
        By.XPATH,
        "//*[@type='file' and @id='manifest-file-field']"),
    "rhci.manifest_upload_button": (
        By.XPATH,
        "//button[text()='Upload']"),
    "rhci.manifest_upload_success": (
        By.XPATH,
        "//*[contains(@class, 'alert-success')]"),
})
