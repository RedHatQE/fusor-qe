from selenium.webdriver.common.by import By
from pages.qci_page import QCIPage


class InstallationSummary(QCIPage):

    # locators
    _view_deployments_loc = (By.XPATH, "//a[contains(.,'View Deployments')]")

    # elements

    @property
    def view_deployments_button(self):
        return self.selenium.find_element(*self._view_deployments_loc)

    # actions

    def click_view_deployments(self):
        from pages.deployments import DeploymentsPage
        self.view_deployments_button.click()
        return DeploymentsPage(self.base_url, self.selenium)
