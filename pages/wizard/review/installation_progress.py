from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pages.qci_page import QCIPage


class InstallationProgress(QCIPage):

    # locators
    _overview_tab_loc = (By.XPATH, '//li[contains(@class,"ember-view")]/a[text()="Overview"]')
    _details_tab_loc = (By.XPATH, '//li[contains(@class,"ember-view")]/a[text()="Details"]')
    _log_tab_loc = (By.XPATH, '//li[contains(@class,"ember-view")]/a[text()="Log"]')

    _error_checkbox_loc = (By.XPATH, '//input[@name="error"]')
    _warn_checkbox_loc = (By.XPATH, '//input[@name="warn"]')
    _info_checkbox_loc = (By.XPATH, '//input[@name="info"]')
    _debug_checkbox_loc = (By.XPATH, '//input[@name="debug"]')
    _logs_dropdown_loc = (By.XPATH, '//select[@id="log-file-select"]')

    _progress_bar_all = (By.XPATH, '//div[@role="progressbar"]')
    _progress_bar_satellite = (By.XPATH, '//div[@class="ember-view row"]/div[contains(@class, "rhci-review-product-name")]/h3[text()="Satellite"]/../..//div[@role="progressbar"]')
    _progress_bar_rhv = (By.XPATH, '//div[@class="ember-view row"]/div[contains(@class, "rhci-review-product-name")]/h3[text()="RHV"]/../..//div[@role="progressbar"]')
    _progress_bar_cloudforms = (By.XPATH, '//div[@class="ember-view row"]/div[contains(@class, "rhci-review-product-name")]/h3[text()="CloudForms"]/../..//div[@role="progressbar"]')
    _progress_bar_openshift = (By.XPATH, '//div[@class="ember-view row"]/div[contains(@class, "rhci-review-product-name")]/h3[text()="OpenShift"]/../..//div[@role="progressbar"]')
    _progress_bar_openstack = (By.XPATH, '//div[@class="ember-view row"]/div[contains(@class, "rhci-review-product-name")]/h3[text()="OpenStack"]/../..//div[@role="progressbar"]')

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
    def progress_bar_satellite(self):
        return self.selenium.find_element(*self._progress_bar_satellite)

    @property
    def progress_bar_rhv(self):
        return self.selenium.find_element(*self._progress_bar_rhv)

    @property
    def progress_bar_cloudforms(self):
        return self.selenium.find_element(*self._progress_bar_cloudforms)

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

    def deployment_complete(self):
        return False

    def deployment_result(self):
        """
        Check the result of all products being deployed.
        Return True if deployment was successful, False otherwise
        """
        return False

    def satellite_success(self):
        """
        Return True if Satellite progress is successful, False otherwise
        """
        return False

    def rhv_success(self):
        """
        Return True if Satellite progress is successful, False otherwise
        """
        return False

    def cloudforms_success(self):
        """
        Return True if Satellite progress is successful, False otherwise
        """
        return False

    def openshift_success(self):
        """
        Return True if Satellite progress is successful, False otherwise
        """
        return False

    def openstack_success(self):
        """
        Return True if Satellite progress is successful, False otherwise
        """
        return False
