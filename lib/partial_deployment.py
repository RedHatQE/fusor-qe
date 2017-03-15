from lib.deployment_runner import UIDeploymentRunner
import copy

def CreatePartialDeployment(new_deployment_pg, deployment_config, name):
    '''
    This routine goes just far enough in creating a deployment for it
    to be saved to the database.   It assumes you are on the product
    selection page.

    It takes the following parameters:

        new_deployment_pg - A pages.wizard.product_selection object.
        deployment_config - A lib.deployment_config object.
        name              - The name of the deployment to create.

    '''
    # Make a copy of the config and set the name to the one that
    # was past in.
    my_config = copy.deepcopy(deployment_config)
    my_config.sat.sat_name = name

    # Now do just enough of the deployment so that it will be saved
    # in the database.   That means do up to the setting of insights and
    # and then cancel out and save.
    runner = UIDeploymentRunner(deployment_config=my_config)
    deployment_name_pg = runner.product_selection(new_deployment_pg)
    update_availability_pg = runner.deployment_name(deployment_name_pg)
    insights_pg = runner.update_availability(update_availability_pg)
    next_pg = runner.access_insights(insights_pg)

    # We've gone far enough, let's cancel and save:
    next_pg.click_cancel()
    next_pg.click_exit_and_save()
