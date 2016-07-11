from selenium.webdriver.common.by import By
from pages.base import Base


class DeploymentName(Base):
    _page_title = "Deployment Name"

    # locators
    _name_loc = (By.ID, 'deployment_new_sat_name')
    _description_loc = (By.ID, 'deployment_new_sat_desc')

    # properties
    @property
    def name(self):
        return self.selenium.find_element(*self._name_loc)

    @property
    def description(self):
        return self.selenium.find_element(*self._description_loc)

    # actions
    def set_name(self, name):
        self.name.send_keys(name)

    def set_description(self, description):
        self.description.send_keys(description)

    def click_back(self):
        from pages.wizard.product_selection import SelectProductsPage
        return super(DeploymentName, self).click_back(
            lambda: SelectProductsPage(self.base_url, self.selenium)
        )

    def click_next(self):
        from pages.wizard.satellite.update_availability import UpdateAvailability
        return super(DeploymentName, self).click_next(
            lambda: UpdateAvailability(self.base_url, self.selenium)
        )

