#
# $Id$
#
from selenium.webdriver.common.by import By

from base import Base


class PageHeader(Page):
    """White header below Nav-bar-inner and above Sidebars:
    1) QCI deployment title
    2) RHCI steps progress

    White background, grey text (blue text for current step)"""

    _page_title = "QuickStart Cloud Installer"

    # page-header-rhci

    # rhci-steps

    # 1. Satellite

    # 2. RHEV

    # 3. Subscriptions

    # 4. Review

# end class PageHeader
