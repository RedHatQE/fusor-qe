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

    _progress_bar_class_success_name = 'progress-bar-success'
    _progress_bar_class_error_name = 'progress-bar-danger'
    _progress_bar_all = (By.XPATH, '//div[@role="progressbar"]')

    _progress_bar_satellite_row = (By.XPATH, '//div[@class="ember-view row"]/div[contains(@class, "rhci-review-product-name")]/h3[text()="Satellite"]/../..')
    _progress_bar_satellite = (By.XPATH, '{}//div[@role="progressbar"]'.format(_progress_bar_satellite_row[1]))
    _progress_bar_satellite_label = (By.XPATH, '{}//div[@class="progress-bar-label"]'.format(_progress_bar_satellite_row[1]))

    _progress_bar_rhv_row = (By.XPATH, '//div[@class="ember-view row"]/div[contains(@class, "rhci-review-product-name")]/h3[text()="RHV"]/../..')
    _progress_bar_rhv = (By.XPATH, '{}//div[@role="progressbar"]'.format(_progress_bar_rhv_row[1]))
    _progress_bar_rhv_label = (By.XPATH, '{}//div[@class="progress-bar-label"]'.format(_progress_bar_rhv_row[1]))

    _progress_bar_cloudforms_row = (By.XPATH, '//div[@class="ember-view row"]/div[contains(@class, "rhci-review-product-name")]/h3[text()="CloudForms"]/../..')
    _progress_bar_cloudforms = (By.XPATH, '{}//div[@role="progressbar"]'.format(_progress_bar_cloudforms_row[1]))
    _progress_bar_cloudforms_label = (By.XPATH, '{}//div[@class="progress-bar-label"]'.format(_progress_bar_cloudforms_row[1]))

    _progress_bar_openshift_row = (By.XPATH, '//div[@class="ember-view row"]/div[contains(@class, "rhci-review-product-name")]/h3[text()="OpenShift"]/../..')
    _progress_bar_openshift = (By.XPATH, '{}//div[@role="progressbar"]'.format(_progress_bar_openshift_row))
    _progress_bar_openshift_label = (By.XPATH, '{}//div[@class="progress-bar-label"]'.format(_progress_bar_openshift_row))

    _progress_bar_openstack_row = (By.XPATH, '//div[@class="ember-view row"]/div[contains(@class, "rhci-review-product-name")]/h3[text()="RHOSP"]/../..')
    _progress_bar_openstack = (By.XPATH, '{}//div[@role="progressbar"]'.format(_progress_bar_openstack_row))
    _progress_bar_openstack_label = (By.XPATH, '{}//div[@class="progress-bar-label"]'.format(_progress_bar_openstack_row))

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
    def progress_bar_all(self):
        return self.selenium.find_elements(*self._progress_bar_all)

    @property
    def progress_bar_satellite(self):
        return self.selenium.find_element(*self._progress_bar_satellite)

    @property
    def progress_bar_satellite_label(self):
        return self.selenium.find_element(*self._progress_bar_satellite_label)

    @property
    def progress_bar_rhv(self):
        return self.selenium.find_element(*self._progress_bar_rhv)

    @property
    def progress_bar_rhv_label(self):
        return self.selenium.find_element(*self._progress_bar_rhv_label)

    @property
    def progress_bar_cloudforms(self):
        return self.selenium.find_element(*self._progress_bar_cloudforms)

    @property
    def progress_bar_cloudforms_label(self):
        return self.selenium.find_element(*self._progress_bar_cloudforms_label)

    @property
    def progress_bar_openshift(self):
        return self.selenium.find_element(*self._progress_bar_openshift)

    @property
    def progress_bar_openshift_label(self):
        return self.selenium.find_element(*self._progress_bar_openshift_label)

    @property
    def progress_bar_openstack(self):
        return self.selenium.find_element(*self._progress_bar_openstack)

    @property
    def progress_bar_openstack_label(self):
        return self.selenium.find_element(*self._progress_bar_openstack_label)

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
        """
        Iterate through all of the progress bars on the page and return true if there is an error
        or all are successful
        """
        all_success = True
        error_found = False

        for progress_bar in self.progress_bar_all:
            if self._progress_bar_class_success_name not in progress_bar.get_attribute('class'):
                all_success = False

            if self._progress_bar_class_error_name in progress_bar.get_attribute('class'):
                error_found = True

        return error_found or all_success

    def deployment_result(self):
        """
        Check the result of all products being deployed.
        Return True if deployment was successful, False otherwise
        """
        result = True
        for progress_bar in self.progress_bar_all:
            if self._progress_bar_class_success_name not in progress_bar.get_attribute('class'):
                result = False

        return result

    def satellite_success(self):
        """
        Return True if Satellite progress is successful, False otherwise
        """
        return (self._progress_bar_class_success_name in
                self.progress_bar_satellite.get_attribute('class'))

    def rhv_success(self):
        """
        Return True if Satellite progress is successful, False otherwise
        """
        return (self._progress_bar_class_success_name in
                self.progress_bar_rhv.get_attribute('class'))

    def cloudforms_success(self):
        """
        Return True if Satellite progress is successful, False otherwise
        """
        return (self._progress_bar_class_success_name in
                self.progress_bar_cloudforms.get_attribute('class'))

    def openshift_success(self):
        """
        Return True if Satellite progress is successful, False otherwise
        """
        return (self._progress_bar_class_success_name in
                self.progress_bar_openshift.get_attribute('class'))

    def openstack_success(self):
        """
        Return True if Satellite progress is successful, False otherwise
        """
        return (self._progress_bar_class_success_name in
                self.progress_bar_openstack.get_attribute('class'))
