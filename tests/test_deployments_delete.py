# This test simply creates a deployment, and then deletes it.
# It does not try to run the deployment, and just fills in enough
# information to get the deployment to be saved to the QCI database,
# and thus show up in the deployments screen, such that we can delete
# it from there.
from pages.deployments import DeploymentsPage
from lib.partial_deployment import CreatePartialDeployment
import time

deployment_name = 'delete me'

def test_deployments_delete(deployments_pg, deployment_config):
    assert isinstance(deployments_pg, DeploymentsPage)

    # Navigate to the product selection page for a new deployment.
    new_deployment_pg = deployments_pg.header.site_navigation_menu("QuickStart Cloud Installer").\
        sub_navigation_menu("New Deployment").click()

    # Create the partial deployment.
    CreatePartialDeployment(
        new_deployment_pg=new_deployment_pg,
        deployment_config=deployment_config,
        name=deployment_name,
    )

    # Seach for the deployment (i.e. make sure it really was created).
    found = deployments_pg.get_deployment(deployment_name)
    assert found is not None

    # Delete the deployment.
    deployments_pg.delete_deployment(deployment_name)

    # Wait a moment for the deployment to go away.
    time.sleep(1)

    # Make sure its gone
    found = deployments_pg.get_deployment(deployment_name)
    assert found is None
