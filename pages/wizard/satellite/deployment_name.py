from selenium.webdriver.common.by import By
from pages.base import Base


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
        return DashboardPage(self.base_url, self.selenium)
        # XXX: If we have navigated to the insights page then
        #      the three choice modal frame will open.
        #      See Jira card:
        #
        #           https://projects.engineering.redhat.com/browse/RHCIQE-124

    def click_back(self):
        self.backBtn.click()
        # XXX: Need add code to return the previous page object.
        #      This will be handled by the DeploymentTaskBar
        #      In this case though it should be the product selection
        #      page.

    def click_next(self):
        self.nextBtn.click()
        return UpdateAvailability(self.base_url, self.selenium)

# These libraries are loaded so we can instantiate their objects after
# the navigational buttons are clicked.
# Also these libraries have to be loaded after our class is defined, because
# we have circular dependencies on one another.
from pages.wizard.satellite.update_availability import UpdateAvailability
from pages.dashboard import DashboardPage
