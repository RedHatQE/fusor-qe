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

        # TODO: We should make the page object for the Deployments page support
        #      handing back simply python structures of the deployment records.
        #
        # Verify it exists
        # 1) Get list of deployments, this will actually be a list of the tr web
        #    elements, the deployments table.
        deployments = deployments_pg.deployments

        # 2) Iterate over the list of deployments and see if the specified name exists.
        found = 0
        for deployment in deployments:
            # 3) Get the text from the first column (that is the deployment name):
            q_dep_name = deployment.find_elements_by_css_selector('td')[0].text

            # 4) See if we found the deployment:
            if q_dep_name == dep_name:
                found = 1
                break

        assert found == 1

    # Iterate over the filters and see if we get the results we want:
    for filter_test in filter_tests:
        pattern = filter_test['filter'] # filter is a reserved word in python.
        rows = filter_test['rows']

        deployments = deployments_pg.search_deployments(pattern)

        assert len(deployments) == rows

    # TODO: Add cleanup code
