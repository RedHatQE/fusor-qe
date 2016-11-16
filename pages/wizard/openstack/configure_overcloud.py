# Page Object Class for "RHOSP:Configure Overcloud"
#
# This page is used to configure:
#
#   - various networking items for the overcloud
#   - undercloud password
#   - ceph storage information
#
from selenium.webdriver.common.by import By
from pages.qci_page import QCIPage


class ConfigureOvercloud(QCIPage):
    _page_title = "QuickStart Cloud Installer"

    ############
    # locators #
    ############
    _external_net_interface_loc = (By.XPATH, "//input[@id = 'external-osp-interface']")
    _private_net_loc = (By.XPATH, "//input[@id = 'osp-private-network']")
    _floating_ip_net_loc = (By.XPATH, "//input[@id = 'osp-floating-network']")
    _floating_ip_net_gateway_loc = (By.XPATH, "//input[@id = 'osp-float-gatewway']")
    _admin_password_loc = (By.XPATH, "//input[@id = 'osp_overcloud_password']")
    _confirm_admin_password_loc = (By.XPATH, "//input[@id = 'confirm_osp_overcloud_password']")
    _external_ceph_storage_loc = (By.XPATH, "//input[@id = 'ospCephStorageCheckbox']")

    # Ceph storage locators
    _ceph_external_mon_host_loc = (By.XPATH, "//input[@id = 'cephExternalMonHostInput']")
    _ceph_cluster_fsid_loc = (By.XPATH, "//input[@id = 'cephClusterFSIDInput']")
    _ceph_client_username_loc = (By.XPATH, "//input[@id = 'cephClientUsernameInput']")
    _ceph_client_key_loc = (By.XPATH, "//input[@id = 'cephClientKeyInput']")
    _nova_rbd_pool_name_loc = (By.XPATH, "//input[@id = 'novarRbdPoolNameInput']")
    _cinder_rbd_pool_name_loc = (By.XPATH, "//input[@id = 'cinderRbdPoolNameInput']")
    _glance_rbd_pool_name_loc = (By.XPATH, "//input[@id = 'glanceRbdPoolNameInput']")

    ##############
    # properties #
    ##############
    @property
    def external_net_interface(self):
        return self.selenium.find_element(*self._external_net_interface_loc)

    @property
    def private_net(self):
        return self.selenium.find_element(*self._private_net_loc)

    @property
    def floating_ip_net(self):
        return self.selenium.find_element(*self._floating_ip_net_loc)

    @property
    def floating_ip_net_gateway(self):
        return self.selenium.find_element(*self._floating_ip_net_gateway_loc)

    @property
    def admin_password(self):
        return self.selenium.find_element(*self._admin_password_loc)

    @property
    def confirm_admin_password(self):
        return self.selenium.find_element(*self._confirm_admin_password_loc)

    @property
    def external_ceph_storage(self):
        return self.selenium.find_element(*self._external_ceph_storage_loc)

    # Ceph storage properties
    @property
    def ceph_external_mon_host(self):
        return self.selenium.find_element(*self._ceph_external_mon_host_loc)

    @property
    def ceph_cluster_fsid(self):
        return self.selenium.find_element(*self._ceph_cluster_fsid_loc)

    @property
    def ceph_client_username(self):
        return self.selenium.find_element(*self._ceph_client_username_loc)

    @property
    def ceph_client_key(self):
        return self.selenium.find_element(*self._ceph_client_key_loc)

    @property
    def nova_rbd_pool_name(self):
        return self.selenium.find_element(*self._nova_rbd_pool_name_loc)

    @property
    def cinder_rbd_pool_name(self):
        return self.selenium.find_element(*self._cinder_rbd_pool_name_loc)

    @property
    def glance_rbd_pool_name(self):
        return self.selenium.find_element(*self._glance_rbd_pool_name_loc)

    ###########
    # actions #
    ###########
    def set_external_net_interface(self, text):
        self.external_net_interface.clear()
        self.external_net_interface.send_keys(text)

    def set_private_net(self, text):
        self.private_net.clear()
        self.private_net.send_keys(text)

    def set_floating_ip_net(self, text):
        self.floating_ip_net.clear()
        self.floating_ip_net.send_keys(text)

    def set_floating_ip_net_gateway(self, text):
        self.floating_ip_net_gateway.clear()
        self.floating_ip_net_gateway.send_keys(text)

    def set_admin_password(self, text):
        self.admin_password.clear()
        self.admin_password.send_keys(text)

    def set_confirm_admin_password(self, text):
        self.confirm_admin_password.clear()
        self.confirm_admin_password.send_keys(text)

    def set_admin_passwords(self, text):
        self.set_admin_password(text)
        self.set_confirm_admin_password(text)

    def click_external_ceph_storage(self):
        self.external_ceph_storage.click()

    # Ceph Actions
    def set_ceph_external_mon_host(self, text):
        self.ceph_external_mon_host.clear()
        self.ceph_external_mon_host.send_keys(text)

    def set_ceph_cluster_fsid(self, text):
        self.ceph_cluster_fsid.clear()
        self.ceph_cluster_fsid.send_keys(text)

    def set_ceph_client_username(self, text):
        self.ceph_client_username.clear()
        self.ceph_client_username.send_keys(text)

    def set_ceph_client_key(self, text):
        self.ceph_client_key.clear()
        self.ceph_client_key.send_keys(text)

    def set_nova_rbd_pool_name(self, text):
        self.nova_rbd_pool_name.clear()
        self.nova_rbd_pool_name.send_keys(text)

    def set_cinder_rbd_pool_name(self, text):
        self.cinder_rbd_pool_name.clear()
        self.cinder_rbd_pool_name.send_keys(text)

    def set_glance_rbd_pool_name(self, text):
        self.glance_rbd_pool_name.clear()
        self.glance_rbd_pool_name.send_keys(text)
