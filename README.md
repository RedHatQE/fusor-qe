# fusor-qe

This repo is for code to test the QCI product (Quickstart Cloud
Installer).   The QCI product runs inside of Satellite, and 
provides an easier way to deploy some Red Hat products:

* RHV (RedHat Virtualization)
* OSP (Open Stack)
* CFME (Cloud Forms)
* OSE  (Open Shift)

# Files/Directories

This section describes the top level files and directories in 
this repository.

## Directories

* docs - documentation tree.
* historic - libraries that came from the robottelo repository.
  These are only used for reference for things like locators.
  Will likely be removed some day.
* lib - directory containing common libraries.
* pages - Page object model classes.
* plugin - custom pytest fixtures.
* tests - All of our tests.

## Files
* conftest.py - specifies pytest fixtures location. 
* pytest.ini.example - example config for pytest.
* README.md - this file.
* requirements.txt - python libraries needed by this repository.
* setup.cfg 
* variables.json.example - contains data needed by the tests.

# Updating Python Requirements

If you want to just update the python libraries on your box, then become
root, go to the root of this source tree, and run the command:

    pip install -r requirements.txt

If however you want use a python virtual environment (see 
https://virtualenv.pypa.io/en/stable/) then you can use this set 
of commands:

    virtualenv ${workspace}.venv
    . ${workspace}.venv/bin/activate
    pip install -r requirements.txt

Note, git is configured to ignore files that end in `.venv` and
`.virtenv`, so though adding one of these extensions is not required
it will make it so the virtual environment does not pollute your
`git status` calls.

A really good guide to learning about virtual environments is:

    http://docs.python-guide.org/en/latest/dev/virtualenvs/

# Checking source against pep8 standard

You can use the flake8 program to verify that source adheres to the
pep8 standard.  To do so with the configuration for this repo run:

    flake8 --config=setup.cfg $src

or:

    flake8 --config=setup.cfg $srcDir


# Testing

Presently testing is broken down into:

* GUI testing
* API testing

All tests use the [pytest framework](http://pytest.org/latest/).

## GUI Testing

We use selenium to test the web UI of the QCI menus/wizards.
To do this effectively we have used the 
[Page Object Model](http://martinfowler.com/bliki/PageObject.html)
to define classes allowing access to each of the gui pages.

## API Testing

These tests use fusor REST api to test QCI.

## Using jupyter notebook

jupyter notebook is fine way to develop tests and page objects.
With it you can run an interactive python shell that is very 
conducive to debugging code.

Once you have jupyter and notebook installed, you will want to 
go to the root of this source repo, and start it:

    jupyter notebook

Then start up a python2 notebook.   After doing this, the following code
can be pasted into a cell, and will get you to the point of having logged 
into QCI:

    url = 'https://10.8.196.250'
    login = 'admin'
    passwd = 'changeme'
    from selenium import webdriver              
    from selenium.webdriver.common.by import By 
    import sys
    sys.path.append(".")
    driver = webdriver.Firefox()
    driver.get(url)
    from pages.login import LoginPage
    loginPage = LoginPage(url, driver)
    dashboard = loginPage.login(login, passwd)

To start a new deployment you would do:  

    selectProducts = dashboard.header\
        .site_navigation_menu('QuickStart Cloud Installer')\
        .sub_navigation_menu('New Deployment')\
        .click()

And to go to the deployments page you would do:

    deployments = dashboard.header\
        .site_navigation_menu('QuickStart Cloud Installer')\
        .sub_navigation_menu('Deployments')\
        .click()

Note you will need to change the url, login and passwd to match your 
installation.

