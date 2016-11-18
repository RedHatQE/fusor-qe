# QCI-97

# In the "Select products to deploy screen, there is a text box to the right
# of the products list.   It as you select various products will contain text
# that explains what is required by each product selected.   Be sure the text
# is correct for the products selected.

def test_product_requirements_text(new_deployment_pg, expected_text):
    prod_expected_txt = expected_text['product_selection_pg_req_box']
    assert new_deployment_pg.\
        get_requirements('general') == \
        prod_expected_txt['general_expected_text']
    assert new_deployment_pg.\
        get_requirements('rhv') == \
        prod_expected_txt['rhv_expected_text']
    assert new_deployment_pg.\
        get_requirements('osp') == \
        prod_expected_txt['osp_expected_text']
    assert new_deployment_pg.\
        get_requirements('cfme') == \
        prod_expected_txt['cfme_expected_text']
    assert new_deployment_pg.\
        get_requirements('ocp') == \
        prod_expected_txt['ocp_expected_text']
    assert new_deployment_pg.\
        get_requirements('disconnected') == \
        prod_expected_txt['disconnected_expected_text']
