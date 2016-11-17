# QCI-93

# Can click on QuickStart Cloud Installer -> Deployments and then press the
# "New Deployment" button.

from pages.deployments import DeploymentsPage
from pages.wizard.product_selection import SelectProductsPage

def test_deployments_button(deployments_pg):
    assert isinstance(deployments_pg, DeploymentsPage)
    new_deployment_pg = deployments_pg.create_new_deployment()
    assert isinstance(new_deployment_pg, SelectProductsPage)
