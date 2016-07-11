from selenium.webdriver.common.by import By
from pages.base import Base


class DeploymentName(Base):
    _page_title = "Deployment Name"

    # locators
    _name_loc = (By.ID, 'deployment_new_sat_name')
    _description_loc = (By.ID, 'deployment_new_sat_desc')
    _password_loc = (By.ID, 'common-password')
    _confirm_password_loc = (By.ID, 'confirm-common-password')

    # properties
    @property
    def name(self):
        return self.selenium.find_element(*self._name_loc)

    @property
    def description(self):
        return self.selenium.find_element(*self._description_loc)

    @property
    def password(self):
        return self.selenium.find_element(*self._password_loc)

    @property
    def confirm_password(self):
        return self.selenium.find_element(*self._confirm_password_loc)

    # actions
    def set_name(self, name):
        self.name.send_keys(name)

    def set_description(self, description):
        self.description.send_keys(description)

    def set_password(self, password):
        self.password.send_keys(password)

    def set_confirm_password(self, password):
        self.confirm_password.send_keys(password)
