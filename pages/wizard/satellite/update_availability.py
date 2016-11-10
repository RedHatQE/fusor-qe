from selenium.webdriver.common.by import By
from pages.base import Base


class UpdateAvailability(Base):
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

    # actions
    def click_immediately(self):
        self.immediately.click()

    def click_after_publishing(self):
        self.after_publishing.click()

    def click_library(self):
        self.library.click()

    def click_new_environment_path(self):
        self.new_environment_path.click()
