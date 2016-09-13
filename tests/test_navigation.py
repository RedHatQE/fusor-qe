
def test_navigate_to_deployments_page(deployments_pg):
    '''
    Tests that a user can navigate to the Deployments page
    from the header menu
    '''
    assert deployments_pg.is_the_current_page

def test_navigate_to_new_deployment_page(new_deployment_pg):
    '''
    Tests that a user can navigate to the New Deployment page
    from the header menu
    '''
    assert new_deployment_pg.is_the_current_page

def test_click_new_deployment_button(deployments_pg):
    '''
    Tests that from the deployments page, a user can click on
    the New Deployment button and get taken to the Product
    Selection page.
    '''
    selectproducts_pg = deployments_pg.create_new_deployment()
    assert selectproducts_pg.is_the_current_page
