from selenium.webdriver.common.by import By
from pages.base import Base

from pages.wizard.regions.deployment_step_bar import DeploymentStepBar

class Insights(Base):
    _page_title = "Insights"

    # locators
    _enable_loc = (By.NAME, 'enable_access_insights')
    _cancel_loc = (
        By.XPATH,
        '//button[contains(@class,"btn") and contains(., "Cancel")]'
    )
    _back_loc = (
        By.XPATH,
        '//a[contains(@class, "btn") and contains(., "Back")]'
    )
    _next_loc = (
        By.XPATH,
        '//button[contains(@class,"btn") and contains(., "Next")]'
    )

    # These locators for the cancel model frame.   Note since the code
    # is always there we don't need to select the dialogue as its just
    # a frame in the existing page that sometimes is visible.
    _exit_and_delete_loc = (
        By.XPATH,
        '//button[contains(.,"Exit and Delete")]'
    )
    _exit_and_save_loc = (
        By.XPATH,
        '//button[contains(.,"Exit and Save")]'
    )
    _continue_working_loc = (
        By.XPATH,
        '//button[contains(.,"Continue Working")]'
    )

    # properties
    @property
    def enable(self):
        return self.selenium.find_element(*self._enable_loc)

    @property
    def cancelBtn(self):
        return self.selenium.find_element(*self._cancel_loc)

    @property
    def backBtn(self):
        return self.selenium.find_element(*self._back_loc)

    @property
    def nextBtn(self):
        return self.selenium.find_element(*self._next_loc)

    @property
    def exit_and_delete_btn(self):
        return self.selenium.find_element(*self._exit_and_delete_loc)

    @property
    def exit_and_save_btn(self):
        return self.selenium.find_element(*self._exit_and_save_loc)

    @property
    def continue_working_btn(self):
        return self.selenium.find_element(*self._continue_working_loc)

    # actions
    def click_enable(self):
        self.enable.click()

    # Note a modal frame will open when this is clicked, with the
    # buttons:
    #
    #   - Exit and Delete
    #   - Exit and Save
    #   - Continue Working
    #
    # These options may be selected by the corresponding calls:
    #
    #   - click_exit_and_delete()
    #   - click_exit_and_save()
    #   - click_continue_working()
    def click_cancel(self):
        self.cancelBtn.click()

    def click_back(self):
        self.backBtn.click()
        return UpdateAvailability(self.base_url, self.selenium)

    def click_next(self):
        dsb = DeploymentStepBar(self.base_url, self.selenium)
        nextPage = dsb.get_next_page()
        self.nextBtn.click()
        return nextPage

    def click_exit_and_delete(self):
        self.exit_and_delete_btn.click()
        return DashboardPage(self.base_url, self.selenium)

    def click_exit_and_save(self):
        self.exit_and_save_btn.click()
        return DashboardPage(self.base_url, self.selenium)

    def click_continue_working(self):
        self.continue_working_btn.click()

# These libraries are loaded so we can instantiate their objects after
# the navigational buttons are clicked.
# Also these libraries have to be loaded after our class is defined, because
# we have circular dependencies on one another.
from pages.wizard.satellite.update_availability import UpdateAvailability
from pages.dashboard import DashboardPage
