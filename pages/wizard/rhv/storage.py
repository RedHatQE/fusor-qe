from selenium.webdriver.common.by import By
from pages.qci_page import QCIPage


class Storage(QCIPage):
    _page_title = "QuickStart Cloud Installer"
    _nfs_radio_loc = (By.XPATH, "//input[@value='NFS']")
    _gluster_radio_loc = (By.XPATH, "//input[@value='glusterfs']")
    _data_domain_name_loc = (By.ID, "rhev_storage_name")
    _storage_address_loc = (By.ID, "rhev_storage_address")
    _share_path_loc = (By.ID, "rhev_share_path")
    _export_domain_name_loc = (By.ID, "rhev_export_domain_name")
    _export_storage_address_loc = (By.ID, "rhev_export_domain_address")
    _export_share_path_loc = (By.ID, "rhev_export_domain_path")
    # only for self-hosted
    _hosted_domain_name_loc = (By.ID, "hosted_storage_name")
    _hosted_storage_address_loc = (By.ID, "hosted_storage_address")
    _hosted_share_path_loc = (By.ID, "hosted_storage_path")
    _alert_rhv_storage = (By.XPATH, "//div[contains(@class, 'rhci-alert')]")
    _spinner_storage_mount = (By.XPATH, "//div[contains(@class, 'spinner-md')]")
    _spinner_storage_mount_text = (By.XPATH, "//div[contains(@class, 'spinner-md')]/../span[@class='spinner-text' and contains(., 'Trying to mount storage paths')]")

    @property
    def alert_rhv_storage(self):
        return self.selenium.find_element(*self._alert_rhv_storage)

    @property
    def spinner_storage(self):
        return self.selenium.find_element(*self._spinner_storage_mount)

    @property
    def spinner_storage_text(self):
        return self.selenium.find_element(*self._spinner_storage_mount_text)

    @property
    def nfs_radio_button(self):
        return self.selenium.find_element(*self._nfs_radio_loc)

    @property
    def gluster_radio_button(self):
        return self.selenium.find_element(*self._gluster_radio_loc)

    @property
    def data_domain_name_field(self):
        return self.selenium.find_element(*self._data_domain_name_loc)

    @property
    def storage_address_field(self):
        return self.selenium.find_element(*self._storage_address_loc)

    @property
    def share_path_field(self):
        return self.selenium.find_element(*self._share_path_loc)

    @property
    def export_domain_name_field(self):
        return self.selenium.find_element(*self._export_domain_name_loc)

    @property
    def export_storage_address_field(self):
        return self.selenium.find_element(*self._export_storage_address_loc)

    @property
    def export_share_path_field(self):
        return self.selenium.find_element(*self._export_share_path_loc)

    # only for self-hosted
    @property
    def hosted_domain_name_field(self):
        return self.selenium.find_element(*self._hosted_domain_name_loc)

    #        only for self-hosted
    @property
    def hosted_storage_address_field(self):
        return self.selenium.find_element(*self._hosted_storage_address_loc)

    # only for self-hosted
    @property
    def hosted_share_path_field(self):
        return self.selenium.find_element(*self._hosted_share_path_loc)

    def get_alerts(self):
        alerts = self.selenium.find_elements(*self._alert_rhv_storage)
        alert_messages = []

        for alert in alerts:
            alert_messages.append(alert.text)

        return alert_messages

    def click_nfs(self):
        self.nfs_radio_button.click()

    def click_gluster(self):
        self.gluster_radio_button.click()

    def set_data_domain_name(self, data):
        self.data_domain_name_field.clear()
        self.data_domain_name_field.send_keys(data)

    def set_storage_address(self, data):
        self.storage_address_field.clear()
        self.storage_address_field.send_keys(data)

    def set_share_path(self, data):
        self.share_path_field.clear()
        self.share_path_field.send_keys(data)

    def set_export_domain_name(self, data):
        self.export_domain_name_field.clear()
        self.export_domain_name_field.send_keys(data)

    def set_export_storage_address(self, data):
        self.export_storage_address_field.clear()
        self.export_storage_address_field.send_keys(data)

    def set_export_share_path(self, data):
        self.export_share_path_field.clear()
        self.export_share_path_field.send_keys(data)

    def set_hosted_domain_name(self, data):
        self.hosted_domain_name_field.clear()
        self.hosted_domain_name_field.send_keys(data)

    def set_hosted_storage_address(self, data):
        self.hosted_storage_address_field.clear()
        self.hosted_storage_address_field.send_keys(data)

    def set_hosted_share_path(self, data):
        self.hosted_share_path_field.clear()
        self.hosted_share_path_field.send_keys(data)
