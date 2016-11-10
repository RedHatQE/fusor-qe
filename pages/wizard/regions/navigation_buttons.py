from selenium.webdriver.common.by import By
from pages.wizard.regions.task_step_bar import TaskStepBar


class NavigationButtons():
    """
    Implements the controls for the navigation buttons on the
    wizards different pages.   Most pages have:

        - back
        - cancel
        - next

    Clicking cancel will open a modal frame, with the buttons:

       - Exit and Delete
       - Exit and Save
       - Continue Working

    All the locators are contained in here with functions to access
    them.
    """

    def __init__(self, base_url, selenium):
        self.base_url = base_url
        self.selenium = selenium
        self.task_step_bar = TaskStepBar(base_url, selenium)

    # locators:
    _cancel_loc = (
        By.XPATH,
        '(//a|//button)[contains(@class,"btn") and contains(., "Cancel")]'
    )
    _back_loc = (
        By.XPATH,
        '//a[contains(@class, "btn") and contains(., "Back")]'
    )
    _next_loc = (
        By.XPATH,
        '(//a|//button)[contains(@class,"btn") and contains(., "Next")]'
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

    ###########
    # Actions #
    ###########

    def click_back(self):
        # It's important that we get the previous page
        # before we actually click the navigation
        # button, so that when determining where to go we start
        # from where we are:
        prev_page = self.task_step_bar.get_prev_page()
        self.back_btn.click()
        return prev_page

    def click_next(self):
        # It's important that we get the next page
        # before we actually click the navigation
        # button, so that when determining where to go we start
        # from where we are:
        next_page = self.task_step_bar.get_next_page()
        self.next_btn.click()
        return next_page

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

    def click_exit_and_delete(self):
        self.exit_and_delete_btn.click()
        from pages.dashboard import DashboardPage
        return DashboardPage(self.base_url, self.selenium)

    def click_exit_and_save(self):
        self.exit_and_save_btn.click()
        from pages.dashboard import DashboardPage
        return DashboardPage(self.base_url, self.selenium)

    def click_continue_working(self):
        self.continue_working_btn.click()
