import re
import pytest
import string
import random

from lib.api import fusor_api

####################################################################################################
# This contains test designed to verify parts of the fusor api functionality. There will be no full
# deployments just builing up part of a deployment to test the functionality of individual api calls
#
# NOTE: There is some overlap in fixtures from test_api_osp_deployment because we need to refactor
#       how fixtures are shared across tests.
# TODO: Fix how we share fixtures across tests
####################################################################################################


def parse_ip_from_url(url):
    """
    Use a regular expression to parse the IP from a url.
    Will return IP address if not protocol is specified
    This assumes that the url does not use a DNS address
    """
    # Regex groups 1 and 2 will make up the protocol and separator
    # Group 3 will be the IP address
    # Group for will be everything after the IP
    url_pattern = r'((https?)://)?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(.*)'
    re_sult = re.match(url_pattern, url)

    protocol, proto_full, ip, url_tail = re_sult.groups()

    return ip


# TODO: Make this global for all QCI tests
@pytest.fixture(scope="module")
def deployment_name(request):
    dep_name = request.config.getoption("--deployment-name")
    print "Deployment name to test: {}".format(dep_name)
    return dep_name


# TODO: Make this global for all QCI tests
@pytest.fixture(scope="module")
def fusor_admin_username(variables):
    return variables['credentials']['fusor']['username']


# TODO: Make this global for all QCI tests
@pytest.fixture(scope="module")
def fusor_admin_password(variables):
    return variables['credentials']['fusor']['password']


@pytest.fixture(scope="module")
def deployment_id(variables):
    """
    Retrieve deployment id used throughout this test
    Currently just generates a random string
    """
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)])


@pytest.fixture(scope="module")
def osp_api(fusor_admin_username, fusor_admin_password, base_url):
    """
    OSPFusorApi object with methods for accessing/editing OSP deployment objects
    """
    fusor_ip = parse_ip_from_url(base_url)
    return fusor_api.OSPFusorApi(fusor_ip, fusor_admin_username, fusor_admin_password)


def test_create_deployment(osp_api, deployment_id, deployment_name):
    deployment_name = 'pytest-{}-osp-cfme'.format(deployment_id)
    deployment_desc = 'pytest for OSP API deployment'

    assert osp_api.create_deployment(deployment_name, deployment_desc)


def test_list_deployment(osp_api):
    assert osp_api.list_deployments()


def test_delete_deployment(osp_api, deployment_id):
    assert osp_api.delete_deployment()
