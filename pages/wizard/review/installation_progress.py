from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pages.base import Base


class InstallationProgress(Base):

    # locators
    _overview_tab_loc = (By.XPATH, '//li[contains(@class,"ember-view")]/a[text()="Overview"]')
    _details_tab_loc = (By.XPATH, '//li[contains(@class,"ember-view")]/a[text()="Details"]')
    _log_tab_loc = (By.XPATH, '//li[contains(@class,"ember-view")]/a[text()="Log"]')

    _error_checkbox_loc = (By.XPATH, '//input[@name="error"]')
    _warn_checkbox_loc = (By.XPATH, '//input[@name="warn"]')
    _info_checkbox_loc = (By.XPATH, '//input[@name="info"]')
    _debug_checkbox_loc = (By.XPATH, '//input[@name="debug"]')
    _logs_dropdown_loc = (By.XPATH, '//select[@id="log-file-select"]')

    # elements
    @property
    def overview_tab(self):
        return self.selenium.find_element(*self._overview_tab_loc)

    @property
    def details_tab(self):
        return self.selenium.find_element(*self._details_tab_loc)

    @property
    def log_tab(self):
        return self.selenium.find_element(*self._log_tab_loc)

    @property
    def error_checkbox(self):
        return self.selenium.find_element(*self._error_checkbox_loc)

    @property
    def warn_checkbox(self):
        return self.selenium.find_element(*self._warn_checkbox_loc)

    @property
    def info_checkbox(self):
        return self.selenium.find_element(*self._info_checkbox_loc)

    @property
    def debug_checkbox(self):
        return self.selenium.find_element(*self._debug_checkbox_loc)

    @property
    def logs_dropdown(self):
        return Select(self.selenium.find_element(*self._logs_dropdown_loc))

    # actions

    def click_overview_tab(self):
        return self.overview_tab.click()

    def click_details_tab(self):
        return self.details_tab.click()

    def click_log_tab(self):
        return self.log_tab.click()

    def view_log(self, log_file):
        """
        Select log to view from dropdown. Valid choices:
            foreman_log, fusor_log, candlepin_log,
            ansible_log, messages_log
        """
        self.click_log_tab()
        self.logs_dropdown.select_by_value(log_file)
