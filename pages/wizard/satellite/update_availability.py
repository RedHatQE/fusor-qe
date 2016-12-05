from selenium.webdriver.common.by import By
from pages.qci_page import QCIPage


class UpdateAvailability(QCIPage):
    _page_title = "Update Availability"

    # locators
    _immediately_loc = (
        By.XPATH,
        '//div[@class = "ident-radio"]/label/input[@type = "radio" and @value="immediately"]'
    )
    _after_publishing_loc = (
        By.XPATH,
        '//div[@class = "ident-radio"]/label/input[@type = "radio" and @value="after_publishing"]'
    )

    # These two will only show up if after publishing is selected.
    _library_loc = (
        By.XPATH,
        '//input[@value="Library"]'
    )
    _new_environment_path_loc = (
        By.XPATH,
        '//button[contains(.,"New Environment Path")]'
    )

    # Modal dialog locators
    _environment_name_loc = (
        By.XPATH,
        '//div[@class="modal-body"]/div[1]/div/div/div/div/input'
    )
    _environment_label_loc = (
        By.XPATH,
        '//div[@class="modal-body"]/div[2]/div/div/div/div/input'
    )
    _environment_description_loc = (
        By.XPATH,
        '//div[@class="modal-body"]/div[3]/div/div/div/div/textarea'
    )
    _submit_button_loc = (
        By.XPATH,
        '//div[@class="modal-footer"]/button[contains(.,"Submit")]'
    )

    # Error message locator
    # For example when environment path you are creating already exists
    _error_loc = (
        By.XPATH,
        '//div[contains(@class, "alert-danger")]'
    )

    # Success message locator
    _success_loc = (
        By.XPATH,
        '//div[contains(@class, "alert-success")]'
    )

    # properties
    @property
    def immediately(self):
        return self.selenium.find_element(*self._immediately_loc)

    @property
    def after_publishing(self):
        return self.selenium.find_element(*self._after_publishing_loc)

    @property
    def library(self):
        return self.selenium.find_element(*self._library_loc)

    @property
    def new_environment_path(self):
        return self.selenium.find_element(*self._new_environment_path_loc)

    @property
    def environment_name(self):
        return self.selenium.find_element(*self._environment_name_loc)

    @property
    def environment_label(self):
        return self.selenium.find_element(*self._environment_label_loc)

    @property
    def environment_description(self):
        return self.selenium.find_element(*self._environment_description_loc)

    @property
    def submit_button(self):
        return self.selenium.find_element(*self._submit_button_loc)

    @property
    def error(self):
        return self.selenium.find_element(*self._error_loc)

    @property
    def success(self):
        return self.selenium.find_element(*self._success_loc)

    # actions
    def click_immediately(self):
        self.immediately.click()

    def click_after_publishing(self):
        self.after_publishing.click()

    def click_library(self):
        self.library.click()

    def click_new_environment_path(self):
        self.new_environment_path.click()

    def click_submit_button(self):
        self.submit_button.click()

    def set_new_env_name(self, text):
        self.environment_name.send_keys(text)

    def set_new_env_description(self, text):
        self.environment_description.send_keys(text)

    def is_success(self):
        try:
            self.success
        except:
            return False
        return True

    def is_error(self):
        try:
            self.error
        except:
            return False
        return True

    def get_error_text(self):
        if self.is_error:
            return self.error.text
        else:
            return None
