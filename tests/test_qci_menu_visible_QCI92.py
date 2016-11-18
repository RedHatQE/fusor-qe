# QCI-92

# QuickStart Cloud Installer plugin menu is visible and clickable

def test_qci_menu_visible(home_page_logged_in):
    home_page_logged_in.header.\
        site_navigation_menu('QuickStart Cloud Installer').\
        hover()
    assert home_page_logged_in.header.\
        site_navigation_menu('QuickStart Cloud Installer').\
        is_menu_submenu_visible
