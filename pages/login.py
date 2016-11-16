from selenium.webdriver.common.by import By
from qci_page import QCIPage


class LoginPage(QCIPage):
    _page_title = "Login"
    # locators
    _login_username_field_locator = (By.ID, 'login_login')
    _login_password_field_locator = (By.ID, 'login_password')
    _login_submit_button_locator = (By.XPATH, '//input[@value="Login"]')

    @property
    def username(self):
        return self.selenium.find_element(*self._login_username_field_locator)

    @property
    def password(self):
        return self.selenium.find_element(*self._login_password_field_locator)

    @property
    def login_button(self):
        return self.selenium.find_element(*self._login_submit_button_locator)

    def _set_login_fields(self, username, password):
        self.username.send_keys(username)
        self.password.send_keys(password)

    def _click_on_login_button(self):
        self.login_button.click()

    def login(self, username, password):
        self._set_login_fields(username, password)
        self._click_on_login_button()
        from pages.dashboard import DashboardPage
        return DashboardPage(self.base_url, self.selenium)
