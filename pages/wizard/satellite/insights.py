from selenium.webdriver.common.by import By
from pages.qci_page import QCIPage


class Insights(QCIPage):
    _page_title = "Insights"

    # locators
    _enable_loc = (By.NAME, 'enable_access_insights')

    # properties
    @property
    def enable(self):
        return self.selenium.find_element(*self._enable_loc)

    # actions
    def click_enable(self):
        self.enable.click()
