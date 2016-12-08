# QCI-98

# In the "Select products to deploy" screen ensure the links are clickable in
# the "To deploy the selected products" panel and that they lead to actual
# pages for the correct versions of the product to deploy.

# We won't actually click on the links, we will just assume that
# access.redhat.com works and instead will just check if the links are
# correct. This is because some of the links require user to be logged-in,
# and that's out of scope for this test.

def test_qci_links_clickable(new_deployment_pg, expected_text):
    links = new_deployment_pg.get_requirement_block_links()

    print expected_text['req_box_links']
    assert cmp(expected_text['req_box_links'], links) == 0
