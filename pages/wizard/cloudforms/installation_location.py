from selenium.webdriver.common.by import By
from pages.base import Base

from pages.wizard.regions.deployment_step_bar import DeploymentStepBar

class InstallationLocation(Base):
    _page_title = "Installation Location"

    # locators
    _install_on_rhv_loc = (By.XPATH, "//input[@value = 'RHEV']")
    _install_on_osp_loc = (By.XPATH, "//input[@value = 'OpenStack']")

    # properties
    @property
    def install_on_rhv(self):
        return self.selenium.find_element(*self._install_on_rhv_loc)

    @property
    def install_on_osp(self):
        return self.selenium.find_element(*self._install_on_osp_loc)

    # actions
    def click_install_on_rhv(self):
        self.install_on_rhv.click()

    def click_install_on_osp(self):
        self.install_on_osp.click()
