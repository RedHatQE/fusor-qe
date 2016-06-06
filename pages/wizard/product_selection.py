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
                                   "//span[@id='is_cloudforms']/div/input")

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
