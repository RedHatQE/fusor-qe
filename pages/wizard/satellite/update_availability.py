#
# $Id$
#
from selenium.webdriver.common.by import By

from base import Base


class UpdateAvailabilityPage(Base):
    """Sidebar right for 1B. Update Availability
    Radio button
    1) Immediately
    2) Tooltip
    3) After manually publishing them
    4) Tooltip"""

    _page_title = "QuickStart Cloud Installer"

    _immediately_radio_button_locator = (
        By.XPATH, "//button[@value='immediately']")

    @property
    def immediately_radio_button_locator(self):
        return self.selenium.find_element(*self._immediately_radio_button_locator)

    _immediately_tooltip_locator = (
        By.XPATH, "//span[@data-toggle='tooltip' and data-original-title='Choosing to not use a lifecycle environment will result in a faster deployment time, but new content will become available to your deployment automatically.  If you use a lifecycle environment, then content needs to be manually published to that environment to be available.']")

    @property
    def immediately_tooltip_desc(self):
        return self.selenium.find_element(*self._immediately_tooltip_locator)

    _after_publishing_radio_button_locator = (
        By.XPATH, "//button[@value='after_publishing']")

    @property
    def after_publishing_radio_button(self):
        return self.selenium.find_element(*self._after_publishing_radio_button_locator)

    _after_publishing_tooltip_locator = (
        By.XPATH, "//span[@data-toogle='tooltip' and data-original-title='For updates to be available within a deployment, they must be published to the lifecycle environment that is assigned to that deployment.']")

    @property
    def after_publishing_tooltip(self):
        return self.selenium.find_element(*self._after_publishing_tooltip_locator)


# end class UpdateAvailabilityPage
