from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base import Base


class SelectProductsPage(Base):
    _page_title = "QuickStart Cloud Installer"
    _rhev_checkbox_locator = (By.XPATH, "//span[@id='is_rhev']/div/input")
    _openstack_checkbox_locator = (By.XPATH,
                                   "//span[@id='is_openstack']/div/input")
    _cloudforms_checkbox_locator = (By.XPATH,
                                    "//span[@id='is_cloudforms']/div/input")
    _openshift_checkbox_locator = (By.XPATH,
                                   "//span[@id='is_openshift']/div/input")
    @property
    def rhev_checkbox(self):
        return self.selenium.find_element(*self._rhev_checkbox_locator)

    @property
    def openstack_checkbox(self):
        return self.selenium.find_element(*self._openstack_checkbox_locator)

    @property
    def cloudforms_checkbox(self):
        return self.selenium.find_element(*self._cloudforms_checkbox_locator)

    @property
    def openshift_checkbox(self):
        return self.selenium.find_element(*self._openshift_checkbox_locator)

    # Navigation Buttons.
    # We need to override base's click_next(), click_back() functions
    # as they all ultimately use the task step bar that does not exist
    # on this page.
    def click_next(self):
        from pages.wizard.satellite.deployment_name import DeploymentName
        self.navigation_buttons.next_btn.click()
        return DeploymentName(self.base_url, self.selenium)

    # there is no back button on this page:
    def click_back(self):
        return None

    @property
    def is_the_current_page(self):
        WebDriverWait(self.selenium, self.timeout).until(
            EC.visibility_of(self.rhev_checkbox),
            "Expected element not present on Select Products Page")
        return True

    def cancel_deployment(self):
        self.click_cancel()
        from pages.deployments import DeploymentsPage
        return DeploymentsPage(self.base_url, self.selenium)
