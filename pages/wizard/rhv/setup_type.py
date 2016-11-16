from selenium.webdriver.common.by import By
from pages.qci_page import QCIPage


class SetupType(QCIPage):
    _page_title = "Setup Type"

    # locators
    _self_hosted_radio_loc = (
        By.XPATH,
        '//input[@type = "radio" and @value = "selfhost"]'
    )
    _hypervisor_engine_radio_loc = (
        By.XPATH,
        '//input[@type = "radio" and @value = "rhevhost"]'
    )

    # properties
    @property
    def self_hosted_btn(self):
        return self.selenium.find_element(*self._self_hosted_radio_loc)

    @property
    def hypervisor_engine_btn(self):
        return self.selenium.find_element(*self._hypervisor_engine_radio_loc)

    # actions
    def click_self_hosted(self):
        self.self_hosted_btn.click()

    def click_hypervisor_engine(self):
        self.hypervisor_engine_btn.click()
