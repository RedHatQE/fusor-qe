# QCI-91

# Can click on QuickStart Cloud Installer -> Deployments and then
# use the filter option to see only the deployments you want to see.
# The test will create various deployments with different names, and
# then apply various filters against them, and see that you only see
# the expected ones.
# "New Deployment" button.
from pages.deployments import DeploymentsPage
from lib.partial_deployment import CreatePartialDeployment

deployment_names = (
    'And Call Him George',
    'Bob',
    'Bushels of Bob',
    'George Martel',
    'There can only be one',
)

filter_tests = (
    {
        'filter': 'Bob',
        'rows': 2,
    },
    {
        'filter': 'George',
        'rows': 2,
    },
    {
        'filter': 'be one',
        'rows': 1,
    },
    {
        'filter': '_____',
        'rows': 0,
    },

)
def test_deployments_button(deployments_pg, deployment_config):
    assert isinstance(deployments_pg, DeploymentsPage)

    # Create all the deployments we will use to test the filter.
    for dep_name in deployment_names:
        # Navigate to the product selection page for a new deployment.
        new_deployment_pg = deployments_pg.header.site_navigation_menu("QuickStart Cloud Installer").\
            sub_navigation_menu("New Deployment").click()

        # Create the partial deployment.
        CreatePartialDeployment(
            new_deployment_pg=new_deployment_pg,
            deployment_config=deployment_config,
            name=dep_name
        )


        # Seach for the deployment (i.e. make sure it really was created).
        found = deployments_pg.get_deployment(dep_name)
        assert found is not None

    # Iterate over the filters and see if we get the results we want:
    for filter_test in filter_tests:
        pattern = filter_test['filter'] # filter is a reserved word in python.
        rows = filter_test['rows']

        deployments = deployments_pg.search_deployments(pattern)

        assert len(deployments) == rows

    # TODO: Add cleanup code
