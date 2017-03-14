"""
This file specifies fixtures that are located under the plugins directory.
Any files added to the plugin directory will need to be listed below for
py.test to load it.
"""
import pytest
from lib.deployment_config import DeploymentConfig

pytest_plugins = "plugin.selenium",\
    "plugin.navigation",\
    "plugin.expected_text"

####################################################################################################
# Command line options available as fixtures for QCI tests
# Options added in pytest_addoption can be used as a fixture in tests
# After add
# In your test case file:
# @pytest.fixture
# def foo_fixture(request):
#     return request.config.getoption("--foo-fixture")
####################################################################################################
def pytest_addoption(parser):
    """
    parser.addoption(
        "--foo-fixture",
        action="store",
        help="Foo thing to do foo stuff with",
        default=None)
    """
    parser.addoption(
        "--deployment-name",
        action="store",
        help="Name of the deployment to test",
        default=None)

    parser.addoption(
        "--qci-expected-text",
        action="store",
        help="File with the expected text lines in json format",
        default=None)

@pytest.fixture
def deployment_config(variables):
    print "*** Create deployment config"
    return DeploymentConfig(conf_dict=variables)
