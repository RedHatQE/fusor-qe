from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base import Base


class DeploymentsPage(Base):
    _page_title = "QuickStart Cloud Installer"
    _search_box_locator = (By.XPATH, '//input[contains(@class, "filter-input")]')
    _search_btn_locator = (By.XPATH, '//button[contains(.,"Search")]')
    _new_deploy_btn_locator = (By.XPATH,
                               '//div[contains(@class, "new-deployment-button")]')
    _deployment_locator = (By.XPATH, '//tr[contains(@class, "deployment-row")]//a[contains(., "{}")]')
    _deployments_locator = (By.XPATH, '//tr[contains(@class, "deployment-row")]')
    _spinner_locator = (By.CLASS_NAME, 'spinner-md')

    # elements
    @property
    def search_box(self):
        return self.selenium.find_element(*self._search_box_locator)

    @property
    def search_button(self):
        return self.selenium.find_element(*self._search_btn_locator)

    @property
    def new_deployment_button(self):
        return self.selenium.find_element(*self._new_deploy_btn_locator)

    @property
    def deployment(self, name):
        strategy, loc = self._deployment_locator
        return self.selenium.find_element(strategy, loc.format(name))

    @property
    def deployments(self):
        return self.selenium.find_elements(*self._deployments_locator)

    @property
    def is_the_current_page(self):
        WebDriverWait(self.selenium, self.timeout).until(
            EC.visibility_of(self.new_deployment_button),
            "Could not find expected element for Deployments Page")
        return True

    # actions
    def create_new_deployment(self):
        self.new_deployment_button.click()
        from pages.wizard.product_selection import SelectProductsPage
        return SelectProductsPage(self.base_url, self.selenium)

    def search_deployments(self, name):
        '''
        Filters deployments using the provided name and returns a list of elements of the results
        '''
        self.search_box.send_keys(name)
        self.search_button.click()
        self.wait_until_element_is_not_visible(self._spinner_locator)
        return self.deployments
