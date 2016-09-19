from selenium.webdriver.common.by import By
from pages.base import Base

from pages.wizard.regions.deployment_step_bar import DeploymentStepBar

class Configuration(Base):
    _page_title = "Configuration"

    # locators
    _root_password_loc = (By.XPATH, "//input[@id = 'cfme_root_password']")
    _confirm_root_password_loc = (By.XPATH, "//input[@id = 'confirm_cfme_root_password']")
    _admin_password_loc = (By.XPATH, "//input[@id = 'cfme_admin_password']")
    _confirm_admin_password_loc = (By.XPATH, "//input[@id = 'confirm_cfme_admin_password']")
    _db_password_loc = (By.XPATH, "//input[@id = 'cfme_db_password']")
    _confirm_db_password_loc = (By.XPATH, "//input[@id = 'confirm_cfme_db_password']")

    # properties
    @property
    def root_password(self):
        return self.selenium.find_element(*self._root_password_loc)

    @property
    def confirm_root_password(self):
        return self.selenium.find_element(*self._confirm_root_password_loc)

    @property
    def admin_password(self):
        return self.selenium.find_element(*self._admin_password_loc)

    @property
    def confirm_admin_password(self):
        return self.selenium.find_element(*self._confirm_admin_password_loc)

    @property
    def db_password(self):
        return self.selenium.find_element(*self._db_password_loc)

    @property
    def confirm_db_password(self):
        return self.selenium.find_element(*self._confirm_db_password_loc)

    # actions
    def set_root_password(self, text):
        self.root_password.clear()
        self.root_password.send_keys(text)

    def set_confirm_root_password(self, text):
        self.confirm_root_password.clear()
        self.confirm_root_password.send_keys(text)

    def set_root_passwords(self, text):
        self.set_root_password(text)
        self.set_confirm_root_password(text)

    def set_admin_password(self, text):
        self.admin_password.clear()
        self.admin_password.send_keys(text)

    def set_confirm_admin_password(self, text):
        self.confirm_admin_password.clear()
        self.confirm_admin_password.send_keys(text)

    def set_admin_passwords(self, text):
        self.set_admin_password(text)
        self.set_confirm_admin_password(text)

    def set_db_password(self, text):
        self.db_password.clear()
        self.db_password.send_keys(text)

    def set_confirm_db_password(self, text):
        self.confirm_db_password.clear()
        self.confirm_db_password.send_keys(text)

    def set_db_passwords(self, text):
        self.set_db_password(text)
        self.set_confirm_db_password(text)
