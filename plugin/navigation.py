import pytest


@pytest.fixture
def home_page_logged_in(base_url, selenium):
    """Logs in to the server and returns the dashboard page."""
    from pages.login import LoginPage
    login_pg = LoginPage(base_url, selenium)
    login_pg.open()
    home_pg = login_pg.login()
    return home_pg
