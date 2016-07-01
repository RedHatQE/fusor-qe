from selenium.webdriver.common.by import By
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
    # navigation buttons
    # XXX: These button are not like all the others.
    #      Instead of being a button they are an anchor.
    _cancel_loc = (
        By.XPATH,
        '//a[contains(@class,"btn") and contains(., "Cancel")]'
    )
    _next_loc = (
        By.XPATH,
        '//a[contains(@class,"btn") and contains(., "Next")]'
    )

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

    @property
    def cancelBtn(self):
        return self.selenium.find_element(*self._cancel_loc)

    @property
    def nextBtn(self):
        return self.selenium.find_element(*self._next_loc)

    def click_cancel(self):
        self.cancelBtn.click()
        return DeploymentsPage(self.base_url, self.selenium)

    def click_next(self):
        self.nextBtn.click()
        return DeploymentName(self.base_url, self.selenium)

# These libraries are loaded so we can instantiate their objects after
# the navigational buttons are clicked.
# Also these libraries have to be loaded after our class is defined, because
# we have circular dependencies on one another.
from pages.wizard.satellite.deployment_name import DeploymentName
from pages.deployments import DeploymentsPage

