from selenium.webdriver.common.by import By
from pages.base import Base

from pages.wizard.regions.deployment_step_bar import DeploymentStepBar

class SetupType(Base):
    _page_title = "Setup Type"

    # locators
    _self_hosted_radio_loc = (
        By.XPATH,
        '//input[@type = "radio" and @value = "selfhost"]'
    )
    _hypervisor_engine_radio_loc = (
        By.XPATH,
        '//input[@type = "radio" and @value = "rhevhost"]'
    )
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
    def self_hosted_btn(self):
        return self.selenium.find_element(*self._self_hosted_radio_loc)

    @property
    def hypervisor_engine_btn(self):
        return self.selenium.find_element(*self._hypervisor_engine_radio_loc)

    @property
    def cancel_btn(self):
        return self.selenium.find_element(*self._cancel_loc)

    @property
    def back_btn(self):
        return self.selenium.find_element(*self._back_loc)

    @property
    def next_btn(self):
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
    def click_self_hosted(self):
        self.self_hosted_btn.click()

    def click_hypervisor_engine(self):
        self.hypervisor_engine_btn.click()

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
        self.cancel_btn.click()

    def click_back(self):
        # Get the last page of the previous deployment step.
        # Must do this before we click back and navigate to
        # that page.
        dsb = DeploymentStepBar(self.base_url, self.selenium)
        prevPage = dsb.get_prev_page()
        self.back_btn.click()
        return prevPage

    def click_next(self):
        self.next_btn.click()
        # XXX: Add return of next page object when next
        # page object is written.

    def click_exit_and_delete(self):
        self.exit_and_delete_btn.click()
        return DashboardPage(self.base_url, self.selenium)

    def click_exit_and_save(self):
        self.exit_and_save_btn.click()
        return DashboardPage(self.base_url, self.selenium)

    def click_continue_working(self):
        self.continue_working_btn.click()
