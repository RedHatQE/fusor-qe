Getting Started
===============

Setup
-----

To use the fusor-qe framework, you'll need to have the necessary dependencies installed.

* [Optional but recommended] Create a virtualenv from which you can run tests.
* Install the necessary python dependencies

  * ``pip install -Ur requirements.txt``
* Copy **pytest.ini.example** to **pytest.ini**
* Copy **variables.json.example** to **variables.json**
* Edit **pytest.ini**, and set base_url to the server under test.

  * ``base_url = https://example.com``
* Edit **variables.json**, and set the admin credentials for the server under test.

Now you are ready to run tests!

Running Tests
-------------

You can run the entire test suite by navigating to the root directory of the
repository and running ``py.test``.

