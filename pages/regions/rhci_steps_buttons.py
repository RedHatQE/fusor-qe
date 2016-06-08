#
# $Id$
#
from selenium.webdriver.common.by import By

from base import Base


class RHCIStepsPage(Base):
    """RHCI Steps Button section at bottom right of page below Sidebar Right and right of Sidebar Left
    White background, grey/black/blue buttons"""

    _page_title = "QuickStart Cloud Installer"

    # RHCI Steps Buttons
    _cancel_button_locator = (By.XPATH, "//button[contains( text(), 'Next' )")

    @property
    def cancel_button(self):
        return self.selenium.find_element(*self._cancel_button_locator)

    _back_button_locator = (By.XPATH, "//button[contains( text(), 'Back' )")

    @property
    def back_button(self):
        return self.selenium.find_element(*self.__back_button_locator)

    _next_button_locator = (By.XPATH, "//button[contains( text(), 'Next' )")

    @property
    def next_button(self):
        return self.selenium.find_element(*self._next_button_locator)


# end class RHCIStepsPage
