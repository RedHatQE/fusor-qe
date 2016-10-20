Getting Started
===============

Setup
-----

To use the fusor-qe framework, you'll need to have the necessary dependencies installed.

* [Optional but recommended] Create a virtualenv from which you can run tests.
* Install the necessary python dependencies

  * ``pip install -Ur requirements.txt``
* Copy **pytest.ini.example** to **pytest.ini**
* Copy **variables.yaml.example** to **variables.yaml**
* Edit **pytest.ini**, and set base_url to the server under test.

  * ``base_url = https://example.com``
* Edit **variables.yaml**, and set the admin credentials for the server under test.

Note: if you are going to run any deployment tests, you'll also need to update the 
**variables.yaml** file to reflect the deployment type and host details for your
particular deployment.

Now you are ready to run tests!

Running Tests
-------------

You can run the entire test suite by navigating to the root directory of the
repository and running ``py.test``. You can also run a specific subset of tests by
pointing directly to the test file. For instance, ``py.test tests/test_login``.

