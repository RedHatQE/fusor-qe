# QCI-131

# Validate new environment name when creating a new environment in library.

# This test uses deployment runner to navigate to the Update Availability page.
# It requires random set of product to be selected and a deployment name to be
# filled in. These are in variables.yaml.

from lib.deployment_runner import UIDeploymentRunner

def test_new_env_path_validation(new_deployment_pg, deployment_config):
    runner = UIDeploymentRunner(deployment_config=deployment_config)
    deployment_name_pg = runner.product_selection(new_deployment_pg)
    update_availability_pg = runner.deployment_name(deployment_name_pg)

    # The submit button should be disabled when no data entered
    update_availability_pg.click_after_publishing()
    update_availability_pg.wait_for_ajax()
    update_availability_pg.click_new_environment_path()
    submit_button = update_availability_pg.submit_button
    is_disabled = submit_button.get_attribute("disabled")
    assert is_disabled

    # New environment path should be created even with 'ugly' characters
    update_availability_pg.set_new_env_name('#&@{}^~[]\|')
    update_availability_pg.click_submit_button()
    if update_availability_pg.is_error():
        raise Exception(update_availability_pg.get_error_text())
    assert update_availability_pg.is_success()

