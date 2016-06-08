#
# $Id$
#
from selenium.webdriver.common.by import By

from base import Base


class SidebarRightPage(Page):
    """Middle right of page: Below Page Header, right of Sidebar Left, and above RHCI Steps Buttons:
    Main input for page.  Common elements.  Actual input is in a separate class (e.g. DeploymentNamePage)

    White background, Black/grey text"""

    _page_title = "QuickStart Cloud Installer"


# end class SideBarRightPage
