from selenium.webdriver.common.by import By
from pages.base import Base


class DetectUndercloud(Base):
    _page_title = "QuickStart Cloud Installer"

    # locators
    _undercloud_ip_loc = (By.XPATH, "//input[@id = 'undercloudIpInput']")
    _ssh_user_loc = (By.XPATH, "//input[@id = 'undercloudSshUserInput']")
    _ssh_password_loc = (By.XPATH, "//input[@id = 'undercloudSshPasswordInput']")
    _detect_undercloud_loc = (By.XPATH, "//button[@id = 'detectUndercloudButton']")
    _new_credentials_loc = (
        By.XPATH,
        "//a[contains(., 'click here to enter new credentials')]"
    )

    # properties
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

    # actions
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
