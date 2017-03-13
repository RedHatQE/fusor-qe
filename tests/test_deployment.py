from time import sleep
from lib.deployment_config import DeploymentConfig
from lib.deployment_runner import UIDeploymentRunner
from pages.wizard.rhv.setup_type import SetupType
from pages.wizard.rhv.engine import Engine
from pages.wizard.openstack.detect_undercloud import DetectUndercloud
from pages.wizard.cloudforms.installation_location import InstallationLocation
from pages.wizard.subscriptions.content_provider import ContentProviderPage
from pages.wizard.subscriptions.review_subscriptions import ReviewSubscriptions
from pages.wizard.review.installation_progress import InstallationProgress
from pages.wizard.openshift.nodes import Nodes


def test_e2e_deployment(new_deployment_pg, variables):
    '''
    Using values from the provided variables file to run a QCI deployment

    This test case mostly handles the logic that determines which page
    we are one and how to proceed through the wizard based on that. The actual
    actions performed on each page and the yaml values that direct those
    actions are handled by the UIDeploymentRunner class.
    '''

    # First parse the config and instantiate the deployment runner
    config = DeploymentConfig()
    runner = UIDeploymentRunner(deployment_config=config)

    # Now navigate through the initial satellite pages
    deployment_name_pg = runner.product_selection(new_deployment_pg)
    update_avail_pg = runner.deployment_name(deployment_name_pg)
    insights_pg = runner.update_availability(update_avail_pg)
    next_pg = runner.access_insights(insights_pg)
    deployment_time_max = variables['deployment'].get('deployment_timeout', 240)

    # Number of retry attempts if there is failure to mount the rhv storage domains
    rhv_storage_fail_retry_max = 3

    # check if we are on the RHV Setup Type page
    if isinstance(next_pg, SetupType):
        setuptype_pg = next_pg
        rhv_hosts_pg = runner.setup_type(setuptype_pg)
        # check if this is a engine + hypervisor deployment
        if isinstance(rhv_hosts_pg, Engine):
            rhv_hyper_pg = runner.engine(rhv_hosts_pg)
        else:
            rhv_hyper_pg = rhv_hosts_pg
        rhv_config_pg = runner.hypervisor(rhv_hyper_pg)
        rhv_storage_pg = runner.rhv_configuration(rhv_config_pg)
        next_pg = runner.rhv_storage(rhv_storage_pg)

        # Attempt to retry the storage mounts if there is a failure
        rhv_storage_mount_failures = 0
        rhv_storage_mount_retry_wait = 3
        while rhv_storage_pg.get_alerts() and rhv_storage_mount_failures < rhv_storage_fail_retry_max:
            rhv_storage_mount_failures += 1
            print "Attempt {}: Alert on RHV storage configuration: {}".format(
                rhv_storage_mount_failures, rhv_storage_pg.alert_rhv_storage.text)
            sleep(rhv_storage_mount_retry_wait)
            next_pg = rhv_storage_pg.click_next()

    # Check if we are on the RHOSP install
    if isinstance(next_pg, DetectUndercloud):
        detect_undercloud_pg = next_pg
        register_nodes_pg = runner.osp_detect_undercloud(detect_undercloud_pg)
        assign_nodes_pg = runner.osp_register_nodes(register_nodes_pg)
        configure_overcloud_pg = runner.osp_assign_nodes(assign_nodes_pg)
        next_pg = runner.osp_configure_overcloud(configure_overcloud_pg)

    # check if we are on the OpenShift node page
    if isinstance(next_pg, Nodes):
        ocp_node_spec_pg = next_pg
        ocp_configuration_pg = runner.ocp_nodes(ocp_node_spec_pg)
        next_pg = runner.ocp_configuration(ocp_configuration_pg)

    # check if we are on the CFME install location page)
    if isinstance(next_pg, InstallationLocation):
        cfmeinstall_pg = next_pg
        cfmeconfig_pg = runner.cfme_install(cfmeinstall_pg)
        next_pg = runner.cfme_config(cfmeconfig_pg)

    # check if we are at the Content Provider Page
    if isinstance(next_pg, ContentProviderPage):
        contentprov_pg = next_pg
        sma_pg = runner.content_provider(contentprov_pg)
        add_subs_pg = runner.subscription_management(sma_pg)
        next_pg = runner.add_subscriptions(add_subs_pg)

    # check if we are at Review Subscriptions page
    # this handles the case where a manifest is already attached
    # and the subscriptions pages in the wizard are skipped
    # TODO: this will need to be revisited once the deployment_step_bar
    # has been updated to handle this situation
    if isinstance(next_pg, ReviewSubscriptions):
        review_subs_pg = next_pg
        review_dep_pg = runner.review_subscriptions(review_subs_pg)
        next_pg = runner.installation_review(review_dep_pg)
        # TODO test that deployment completes via API
        #
        # This just asserts that we have made it to the deployment progress
        # page successfully. To match the functionality of the existing
        # robottelo test, the API will need to track the progress of the
        # deployment from here.
        assert isinstance(next_pg, InstallationProgress)

    if isinstance(next_pg, InstallationProgress):
        install_progress_pg = next_pg
        deployment_time = 0
        deployment_time_wait = 1  # Time (minutes) to poll for deployment status
        while deployment_time < deployment_time_max and not install_progress_pg.deployment_complete():
            sleep(deployment_time_wait * 60)  # Convert minute to seconds
            deployment_time += deployment_time_wait

        assert install_progress_pg.deployment_result(), "Deployment failed after {} minutes".format(deployment_time)

    else:
        # if we aren't at the Review Subscriptions page, something went wrong.
        assert False
