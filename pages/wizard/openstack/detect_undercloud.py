from selenium.webdriver.common.by import By
from pages.base import Base


class DetectUndercloud(Base):
    _page_title = "QuickStart Cloud Installer"

    ############
    # locators #
    ############
    _undercloud_ip_loc = (By.XPATH, "//input[@id = 'undercloudIpInput']")
    _ssh_user_loc = (By.XPATH, "//input[@id = 'undercloudSshUserInput']")
    _ssh_password_loc = (By.XPATH, "//input[@id = 'undercloudSshPasswordInput']")
    _detect_undercloud_loc = (By.XPATH, "//button[@id = 'detectUndercloudButton']")
    _new_credentials_loc = (
        By.XPATH,
        "//a[contains(., 'click here to enter new credentials')]"
    )

    # Overcloud Already Running
    #   When the overcloud is already running after you enter the information
    #   for the undercloud, you will end up with two links displayed:
    #
    #       - Delete overcloud
    #       - use a different undercloud
    _delete_overcloud_loc = (By.XPATH, "//a[contains(., 'Delete overcloud')]")
    _use_different_overcloud_loc = (
        By.XPATH,
        "//a[contains(., 'use a different undercloud')]"
    )

    ##############
    # properties #
    ##############
    @property
    def undercloud_ip(self):
        return self.selenium.find_element(*self._undercloud_ip_loc)

    @property
    def ssh_user(self):
        return self.selenium.find_element(*self._ssh_user_loc)

    @property
    def ssh_password(self):
        return self.selenium.find_element(*self._ssh_password_loc)

    @property
    def detect_undercloud(self):
        return self.selenium.find_element(*self._detect_undercloud_loc)

    @property
    def new_credentials(self):
        return self.selenium.find_element(*self._new_credentials_loc)

    # Overcloud Already Running
    @property
    def delete_overcloud(self):
        return self.selenium.find_element(*self._delete_overcloud_loc)

    @property
    def use_different_overcloud(self):
        return self.selenium.find_element(*self._use_different_overcloud_loc)

    ###########
    # actions #
    ###########
    def set_undercloud_ip(self, text):
        self.undercloud_ip.clear()
        self.undercloud_ip.send_keys(text)

    def set_ssh_user(self, text):
        self.ssh_user.clear()
        self.ssh_user.send_keys(text)

    def set_ssh_password(self, text):
        self.ssh_password.clear()
        self.ssh_password.send_keys(text)

    def click_detect_undercloud(self):
        self.detect_undercloud.click()

    def click_new_credentials(self):
        self.new_credentials.click()

    # Overcloud Already Running
    def click_delete_overcloud(self):
        self.delete_overcloud.click()

    def click_use_different_overcloud(self):
        self.use_different_overcloud.click()
