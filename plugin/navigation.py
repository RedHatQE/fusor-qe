import pytest


def _submenu(home_pg, main_menu, submenu):
    return home_pg.header.site_navigation_menu(main_menu)\
        .sub_navigation_menu(submenu).click()


@pytest.fixture
def home_page_logged_in(base_url, selenium, variables):
    """Logs in to the server and returns the dashboard page."""
    from pages.login import LoginPage
    login_pg = LoginPage(base_url, selenium)
    login_pg.open()
    home_pg = login_pg.login(variables['credentials']['fusor']['username'],
                             variables['credentials']['fusor']['password'])
    return home_pg


@pytest.fixture
def deployments_pg(home_page_logged_in):
    return _submenu(home_page_logged_in,
                    "QuickStart Cloud Installer", "Deployments")


@pytest.fixture
def new_deployment_pg(home_page_logged_in):
    return _submenu(home_page_logged_in,
                    "QuickStart Cloud Installer", "New Deployment")
