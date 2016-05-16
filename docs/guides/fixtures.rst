Fixtures
========

Fixtures are a feature of the py.test library that "provide a fixed baseline
upon which tests can reliably and repeatedly execute." [#]_ They offer a
modular alternative to the usual setup and teardown functions. Py.test can make
use of fixtures in a number of ways, but for the purposes of this guide, we
will only cover how the fusor-qe framework uses them currently. If our usage of
fixtures expands, so will this page.

Py.test includes some useful fixtures out of the box. If you have any py.test
plugins installed, they may add fixtures of their own. You can see a list of
all available fixtures by running:

.. code-block:: bash

   py.test --fixtures

How do I write a fixture?
^^^^^^^^^^^^^^^^^^^^^^^^^

A fixture is just a function that has been marked with the @pytest.fixture decorator.
As an example, consider this test:

.. code-block:: python

  def test_login_admin(base_url, selenium, variables):
      login_pg = LoginPage(base_url, selenium)
      login_pg.open()
      dashboard_pg = login_pg.login(variables['credentials']['fusor']['username'],
                                    variables['credentials']['fusor']['password'])
      assert dashboard_pg.is_the_current_page

This is a simple selenium test that navigates a browser to the application's
login page, fills out the username and password fields, and logs in. It then
asserts that it is on the dashboard page of the application. If the username
and password for the admin user are going to be used frequently in our test
cases, you might want to make a fixture for them so they are easily accessible.

.. code-block:: python

   @pytest.fixture
   def admin_username(variables):
     return variables['credentials']['fusor']['username']

   @pytest.fixture
   def admin_password(variables):
     return variables['credentials']['fusor']['password']

With these new fixtures, the original test becomes:

.. code-block:: python

  def test_login_admin(base_url, selenium, admin_username,
                       admin_password):
      login_pg = LoginPage(base_url, selenium)
      login_pg.open()
      dashboard_pg = login_pg.login(admin_username, admin_password)
      assert dashboard_pg.is_the_current_page

There are a few important things to note about the example above:

* The function arguments *base_url*, *selenium*, *variables*, *admin_username*, and *admin_password* are all fixtures.

  + We created *admin_username* and *admin_password* in the above code.
  + The other three are provided by the **pytest-selenium** and **pytest-variables** plugins.
* Tests can use a fixture by passing in the fixture's function name.
* Fixtures can use other fixtures, too.

In the case above, the *variables* fixture is passed into each of our two
fixture functions. *variables* provides a dictionary (named variables) that
holds the contents of the variables.json file at the root directory of this
repo. Our two fixtures simply return a value from that dictionary.

This only scratches the surface of what can be done with fixtures. Further
details and examples can be found at the link to the py.test documentation in the footnotes.

.. [#] `py.test fixture documentation <https://pytest.org/latest/fixture.html>`_
