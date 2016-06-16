from selenium.webdriver.common.by import By
from pages.base import Base

# This library is loaded so we can instantiate this object after
# the next button is clicked as this is the next page.
from pages.wizard.satellite.insights import Insights

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
    def immediately(self):
        return self.selenium.find_element(*self._immediately_loc)

    @property
    def after_publishing(self):
        return self.selenium.find_element(*self._after_publishing_loc)

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
    def click_immediately(self):
        self.immediately.click()

    def click_after_publishing(self):
        self.after_publishing.click()

    def click_cancel(self):
        self.cancelBtn.click()

    def click_back(self):
        self.backBtn.click()

    def click_next(self):
        self.nextBtn.click()
        return Insights(self.base_url, self.selenium)
