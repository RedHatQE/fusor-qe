#
# $Id$
#
from selenium.webdriver.common.by import By

from base import Base


class CancelDeploymentModalPage(Base):
    """Cancel Deployment Modal Window:
    1) Modal Header
    2) Close button
    3) Modal Body
    4) Modal Footer
    5) Exit and Delete button
    6) Exit and Save button
    7) Continue Working button"""

    _page_title = "QuickStart Cloud Installer"

    _exit_and_delete_button_locator = (
        By.XPATH, "//button[contains( text(), 'Exit and Delete' )")

    @property
    def exit_and_delete(self):
        return self.selenium.find_element(*self._exit_and_delete_button_locator)

    _exit_and_save_button_locator = (
        By.XPATH, "//button[contains( text(), 'Exit and Save' )")

    @property
    def exit_and_save_button(self):
        return self.selenium.find_element(*self._exit_and_delete_button_locator)

    # Continue Working
    _continue_working_button_locator = (
        By.XPATH, "//button[contains( text(), 'Continue Working' )")

    @property
    def continue_working(self):
        return self.selenium.find_element(*self._continue_working_button_locator)

# end class CancelDeploymentModalPage
