from selenium.webdriver.common.by import By
from pages.base import Base

class Configuration(Base):
    _page_title = "QuickStart Cloud Installer"
    _nfs_radio_loc = (By.XPATH, "//input[@value='NFS']")
    _gluster_radio_loc = (By.XPATH, "//input[@value='GFS']")
    _host_field_loc = (By.ID, "openshift_storage_host")
    _export_path_field_loc = (By.ID, "openshift_export_path")
    _username_field_loc = (By.ID, "openshift_username")
    _password_field_loc = (By.ID, "openshift_password")
    _confirm_password_field_loc = (By.ID, "confirm_openshift_password")
    _subdomain_field_loc = (By.ID, "openshift_subdomain_name")
    _hello_world_checkbox_loc = (By.ID, "openshift_hello_world")

    @property
    def nfs_radio(self):
        return self.selenium.find_element(*self._nfs_radio_loc)

    @property
    def gluster_radio(self):
        return self.selenium.find_element(*self._gluster_radio_loc)

    @property
    def host_field(self):
        return self.selenium.find_element(*self._host_field_loc)

    @property
    def export_path_field(self):
        return self.selenium.find_element(*self._export_path_field_loc)

    @property
    def username_field(self):
        return self.selenium.find_element(*self._username_field_loc)

    @property
    def password_field(self):
        return self.selenium.find_element(*self._password_field_loc)

    @property
    def confirm_password_field(self):
        return self.selenium.find_element(*self._confirm_password_field_loc)

    @property
    def subdomain_field(self):
        return self.selenium.find_element(*self._subdomain_field_loc)

    @property
    def hello_world_checkbox(self):
        return self.selenium.find_element(*self._hello_world_checkbox_loc)

    def click_nfs_radio(self):
        self.nfs_radio.click()

    def click_gluster_radio(self):
        self.gluster_radio.click()

    def set_host(self, keys):
        self.host_field.clear()
        self.host_field.send_keys(keys)

    def set_export_path(self, keys):
        self.export_path_field.clear()
        self.export_path_field.send_keys(keys)

    def set_username(self, keys):
        self.username_field.clear()
        self.username_field.send_keys(keys)

    def set_password(self, keys):
        self.password_field.clear()
        self.password_field.send_keys(keys)

    def set_confirm_password(self, keys):
        self.confirm_password_field.clear()
        self.confirm_password_field.send_keys(keys)

    def set_passwords(self, keys):
        self.set_password(keys)
        self.set_confirm_password(keys)

    def set_subdomain(self, keys):
        self.subdomain_field.clear()
        self.subdomain_field.send_keys(keys)

    def click_hello_world(self):
        self.hello_world_checkbox.click()

