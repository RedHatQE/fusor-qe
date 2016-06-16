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
    def cancel(self):
        return self.selenium.find_element(*self._insights_cancel)

    @property
    def back(self):
        return self.selenium.find_element(*self._insights_back)

    @property
    def next(self):
        return self.selenium.find_element(*self._insights_next)

    # actions
    def click_enable(self):
        self.enable.click()


    def click_cancel(self):
        self.cancel.click()

    def click_back(self):
        self.back.click()

    def click_next(self):
        self.next.click()
        # XXX: Need add code to return the next page object.
        #      This is not trivial though and will be handled
        #      by another library.
