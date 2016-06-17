from selenium.webdriver.common.by import By
from pages.base import Base

class Insights(Base):
    _page_title = "Insights"

    # locators
    _insights_enable = (By.NAME, 'enable_access_insights')
    _insights_cancel = (
        By.XPATH,
        '//button[contains(@class,"btn") and contains(., "Cancel")]'
    )
    _insights_back = (
        By.XPATH,
        '//a[contains(@class, "btn") and contains(., "Back")]'
    )
    _insights_next = (
        By.XPATH,
        '//button[contains(@class,"btn") and contains(., "Next")]'
    )

    # properties
    @property
    def enable(self):
        return self.selenium.find_element(*self._insights_enable)

    @property
    def cancelBtn(self):
        return self.selenium.find_element(*self._insights_cancel)

    @property
    def backBtn(self):
        return self.selenium.find_element(*self._insights_back)

    @property
    def nextBtn(self):
        return self.selenium.find_element(*self._insights_next)

    # actions
    def click_enable(self):
        self.enable.click()


    def click_cancel(self):
        self.cancelBtn.click()
        # XXX: This needs some work as a second modal opens when you
        #      click this.


    def click_back(self):
        self.backBtn.click()
        return UpdateAvailability(self.base_url, self.selenium)

    def click_next(self):
        self.nextBtn.click()
        # XXX: Need add code to return the next page object.
        #      This is not trivial though and will be handled
        #      by another library.

# These libraries are loaded so we can instantiate their objects after
# the navigational buttons are clicked.
# Also these libraries have to be loaded after our class is defined, because
# we have circular dependencies on one another.
from pages.wizard.satellite.update_availability import UpdateAvailability
