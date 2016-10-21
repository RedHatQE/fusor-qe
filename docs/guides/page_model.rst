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

Example Page Object
^^^^^^^^^^^^^^^^^^^

Below is a simplified version of the page object for the
Deployment Name page in the QCI wizard:

.. code-block:: python

   from selenium.webdriver.common.by import By
   from pages.base import Base

   class DeploymentName(Base):

       # locators
       _name_loc = (By.ID, 'deployment_new_sat_name')
       _description_loc = (By.ID, 'deployment_new_sat_desc')

       # properties
       @property
       def name(self):
           return self.selenium.find_element(*self._name_loc)

       @property
       def description(self):
           return self.selenium.find_element(*self._description_loc)

       # actions
       def set_name(self, name):
           self.name.send_keys(name)

       def set_description(self, description):
           self.description.send_keys(description)

Generally, page objects will follow this format and have three sections:

locators:
    Each actionable element on a page is represented as a tuple of the format:
    *(locator_strategy, locator_string)*. Selenium supports a number of
    strategies for locating elements, and they are all attributes of the By
    class. You can find more information about locating elements here:
    `Locating Elements
    <http://selenium-python.readthedocs.io/locating-elements.html#locating-elements>`_

properties:
    Properties take the defined locators and expose them as a property of the
    class. The value of this becomes clear in the next section.

actions:
    These methods represent the actions that a user can take on a given page.
    In this case, a user can set the name and description of a deployment. As
    the methods above show, this is done by interacting with the properties of
    the class, instead of calling ``page.selenium.find_element()`` everytime we
    want to interact with an element on the page.

Additional Reading
^^^^^^^^^^^^^^^^^^

* https://pragprog.com/magazines/2010-08/page-objects-in-python
* http://martinfowler.com/bliki/PageObject.html
* https://github.com/mozilla/Addon-Tests

