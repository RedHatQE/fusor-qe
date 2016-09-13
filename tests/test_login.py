from pages.login import LoginPage


def test_login_admin(base_url, selenium, variables):
    login_pg = LoginPage(base_url, selenium)
    login_pg.open()
    dashboard_pg = login_pg.login(variables['credentials']['fusor']['username'],
                                  variables['credentials']['fusor']['password'])
    assert dashboard_pg.is_the_current_page
