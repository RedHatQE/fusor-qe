# fusor-qe

This repo is for code to test the QCI product (Quickstart Cloud
Installer).   The QCI product runs inside of Satellite, and 
provides an easier way to deploy some Red Hat products:

* RHEV 
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
