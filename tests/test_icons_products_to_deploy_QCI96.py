# QCI-96

# In the "Select products to deploy" screen, when you hover over the "i" icon
# by each product, text about the product is displayed. This is true whether
# you have the product selected or not.

# We hard coded the text that we are looking for here, knowing that it might
# require that this test get updated fairly often. We chose to do that because
# it does give us a way to automate checking that the text makes sense is
# accurate, as at the time of copying the person copying it made sure of this.
# So we are making a compromise between the need to update this test more often
# against the ability to actually automate the test.

def test_icons_products_to_deploy(new_deployment_pg):
    rhv_expected_text = ("Complete enterprise virtualization management for"
                         " servers and desktops on the same infrastructure")
    osp_expected_text = ("Flexible, secure foundations to build a massively"
                         " scalable private or public cloud")
    cfme_expected_text = ("Manage your virtual, private, and hybrid cloud"
                          " infrastructures")
    ocp_expected_text = ("Develop, host, and scale applications in a cloud"
                         " environment")
    assert new_deployment_pg.get_i_icon_text('rhv') == rhv_expected_text
    assert new_deployment_pg.get_i_icon_text('osp') == osp_expected_text
    assert new_deployment_pg.get_i_icon_text('cfme') == cfme_expected_text
    assert new_deployment_pg.get_i_icon_text('ocp') == ocp_expected_text
