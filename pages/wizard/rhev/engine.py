from selenium.webdriver.common.by import By
from pages.base import Base
from pages.wizard.rhev.hosts import Hosts

class Engine(Base):
    _page_title = "QuickStart Cloud Installer"
    _search_box_loc = (By.XPATH, "//div[@class = 'rhev-search-box']/input[@type = 'text']")
    _refresh_data_loc = (By.XPATH, "//button[contains(.,'Refresh Data')]")
    _host_table_loc = (By.XPATH, "//div[@class = 'col-lg-9']/table")

    @property
    def search_box(self):
        return self.selenium.find_element(*self._search_box_loc)

    @property
    def refresh_data_button(self):
        return self.selenium.find_element(*self._refresh_data_loc)

    @property
    def hosts(self):
        return Hosts(self.selenium.find_element(*self._host_table_loc))

    def search(self, phrase):
        self.search_box.clear()
        self.search_box.send_keys(phrase)

    def click_refresh_data(self):
        self.refresh_data_button.click()

