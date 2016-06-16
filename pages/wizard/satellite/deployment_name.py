from selenium.webdriver.common.by import By
from pages.base import Base

# This library is loaded so we can instantiate this object after
# the next button is clicked as this is the next page.
from pages.wizard.satellite.update_availability import UpdateAvailability

class DeploymentName(Base):
    _page_title = "Deployment Name"

    # locators
    _name_loc = (By.ID, 'deployment_new_sat_name')
    _description_loc = (By.ID, 'deployment_new_sat_desc')
    _cancel_loc = (
        By.XPATH,
        '//button[contains(@class,"btn") and contains(., "Cancel")]'
    )
    _back_loc = (
        By.XPATH,
        '//a[contains(@class, "btn") and contains(., "Back")]',
    )
    _next_loc = (
        By.XPATH,
        '//button[contains(@class,"btn") and contains(., "Next")]'
    )


    # properties
    @property
    def name(self):
        return self.selenium.find_element(*self._name_loc)

    @property
    def description(self):
        return self.selenium.find_element(*self._description_loc)

    @property
    def cancelBtn(self):
        return self.selenium.find_element(*self._cancel_loc)

    @property
    def backBtn(self):
        return self.selenium.find_element(*self._back_loc)

    @property
    def nextBtn(self):
        return self.selenium.find_element(*self._next_loc)

    # actions
    def set_name(self, name):
        self.name.send_keys(name)

    def set_description(self, description):
        self.description.send_keys(description)

    def click_cancel(self):
        self.cancelBtn.click()

    def click_back(self):
        self.backBtn.click()

    def click_next(self):
        self.nextBtn.click()
        return UpdateAvailability(self.base_url, self.selenium)

