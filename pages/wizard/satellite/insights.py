from selenium.webdriver.common.by import By
from pages.base import Base

from pages.wizard.regions.deployment_step_bar import DeploymentStepBar

class Insights(Base):
    _page_title = "Insights"

    # locators
    _enable_loc = (By.NAME, 'enable_access_insights')
    # properties
    @property
    def enable(self):
        return self.selenium.find_element(*self._enable_loc)

    # actions
    def click_enable(self):
        self.enable.click()

    def click_back(self):
        from pages.wizard.satellite.update_availability import UpdateAvailability
        return super(Insights, self).click_back(
            lambda: UpdateAvailability(self.base_url, self.selenium)
        )

    def click_next(self):
        return super(Insights, self).click_next(
            lambda:
                DeploymentStepBar(
                    self.base_url,
                    self.selenium
                ).get_next_page()
        )
