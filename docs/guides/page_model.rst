Page Object Pattern
===================

The Page Obect pattern is based on the idea of building a model for a page that
acts as an interface to the application being tested. Tests that are created in
this model only make use of the method provided by the page objects, and do not
make selenium calls directly. There are many benefits to this. Consider the two
tests below:

.. code-block:: python

   def test_login(url, username, password):
     driver.get(url)
     driver.find_element(By.id, "username").send_keys(username)
     driver.find_element(By.id, "password").send_keys(password)
     driver.find_element(By.id, "submit").click()
     WebDriverWait(driver, 10)
     assert driver.title == "Dashboard"

.. code-block:: python

  def test_login_pop(base_url, username, password):
      login_pg = LoginPage(base_url)
      login_pg.open()
      dashboard_pg = login_pg.login(username, password)
      assert dashboard_pg.is_the_current_page

Whats different about these two approaches? For one thing, ``test_login``
directly uses the selenium object on every single line of the test. It also
hardcodes selenium locators into the test functions. If a locator were to
change, you would need to update every test where that locator is used.

Compare this to ``test_login_pop``. This test creates an instance of the
LoginPage class, opens a browser to that page, logs in with the provided
username and password, and asserts that it is on the dashboard page. It does
essentially the exact same thing as ``test_login``, but it is far more legible.
``test_login_pop`` is describing *what* the test is doing, while ``test_login``
is describing *how* the test is going to do it.

Another notable feature of ``test_login_pop`` is that the login_pg.login()
method returns a dashboard page. This is an important aspect of the page object
pattern: if an action on a page (such as submitting a login form) will lead you
to another page (like the dashboard), then the method (login_pg.login) should
return the appropriate page object. This approach creates a flow between
different pages in the application that should mirror how a user would interact
with the website directly.

Additional Reading
^^^^^^^^^^^^^^^^^^

* https://pragprog.com/magazines/2010-08/page-objects-in-python
* http://martinfowler.com/bliki/PageObject.html
* https://github.com/mozilla/Addon-Tests

