from selenium.webdriver.common.by import By
from pages.base import Base


class ContentProviderPage(Base):

    # locators
    _redhat_cdn_radio_loc = (By.XPATH, '//input[@type="radio" and @value="redhat_cdn"]')
    _disconnected_radio_loc = (By.XPATH,
                               '//input[@type="radio" and @value="disconnected"]')
    _rh_login_field_loc = (By.XPATH, '//input[@id="red-hat-login"]')
    _rh_password_field_loc = (By.XPATH, '//input[@id="portal-password"]')
    _lost_password_loc = (By.XPATH, '//a[contains(@href, "lostPassword")]')
    _content_mirror_url_loc = (By.XPATH, '//input[@id="content-mirror-url"]')
    _browse_manifest_loc = (By.XPATH, '//input[@id="manifest-file-field"]')
    _upload_manifest_loc = (By.XPATH, '//button[contains(., "Upload")]')

    @property
    def redhat_cdn_radio(self):
        return self.selenium.find_element(*self._redhat_cdn_radio_loc)

    @property
    def disconnected_radio(self):
        return self.selenium.find_element(*self._disconnected_radio_loc)

    @property
    def rh_login_field(self):
        return self.selenium.find_element(*self._rh_login_field_loc)

    @property
    def rh_password_field(self):
        return self.selenium.find_element(*self._rh_password_field_loc)

    @property
    def lost_password_link(self):
        return self.selenium.find_element(*self._lost_password_loc)

    @property
    def browse_manifest_button(self):
        return self.selenium.find_element(*self._browse_manifest_loc)

    @property
    def upload_manifest_button(self):
        return self.selenium.find_element(*self._upload_manifest_loc)

    @property
    def disconnected_url_field(self):
        return self.selenium.find_element(*self._content_mirror_url_loc)

    # Actions

    def click_redhat_cdn(self):
        return self.redhat_cdn_radio.click()

    def click_disconnected(self):
        return self.disconnected_radio.click()

    def set_username(self, name):
        self.rh_login_field.clear()
        self.rh_login_field.send_keys(name)

    def set_password(self, password):
        self.rh_password_field.clear()
        self.rh_password_field.send_keys(password)

    def click_lost_pass_link(self):
        return self.lost_password_link.click()

    def select_manifest_file(self, path):
        """ browses and selects a manifest file using the path provided
        """
        self.browse_manifest_button.clear()
        self.browse_manifest_button.send_keys(path)

    def click_upload_manifest(self):
        return self.upload_manifest_button.click()

    def set_disconnected_url_field(self, url):
        self.disconnected_url_field.clear()
        self.disconnected_url_field.send_keys(url)
