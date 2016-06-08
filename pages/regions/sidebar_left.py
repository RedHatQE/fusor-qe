#
# $Id$
#
from selenium.webdriver.common.by import By

from base import Base


class SidebarLeftPage(Page):
    """Left Navigation below Page Header, left of Sidebar Right and RHCI Steps Buttons:
    For the current step, the sub-steps (e.g. for 1. Satellite, will contain:
    1A. Deployment Name
    1B. Update Availability
    1C. Red Hat Insights

    White/blue background, white/grey text"""

    _page_title = "QuickStart Cloud Installer"

    # sidebar-pf-left


# end class SideBarLeftPage
