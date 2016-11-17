# QCI-93

# Can click on QuickStart Cloud Installer -> New Deployment

from pages.wizard.product_selection import SelectProductsPage

def test_new_deployment_button(new_deployment_pg):
    assert isinstance(new_deployment_pg, SelectProductsPage)
