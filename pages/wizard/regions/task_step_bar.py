import re
from selenium.webdriver.common.by import By
from pages.wizard.regions.deployment_step_bar import DeploymentStepBar

# XXX: Still need to fill this out completely.
# Maps task steps to their class and library.
# The deployment step name used to do the mapping is
# the is fully qualified step name (i.e. it contains the
# deployment and task step).   As an example the Configuration
# step in the RHV deployment would have a fully qualified
# step name of RHV.configuration, whereas the Configuration step
# in the CloudForms deployment would have a fully qualified
# step name of CloudForms.Configuration.
_step_to_page_map = {
    'Satellite.Deployment Name': {
        'class': 'DeploymentName',
        'library': 'pages.wizard.satellite.deployment_name',
    },
    'Satellite.Update Availability': {
        'class': 'UpdateAvailability',
        'library': 'pages.wizard.satellite.update_availability',
    },
    'Satellite.Red Hat Insights': {
        'class': 'Insights',
        'library': 'pages.wizard.satellite.insights',
    },
    'RHV.Setup Type': {
        'class': 'SetupType',
        'library': 'pages.wizard.rhv.setup_type',
    },
    'RHV.Engine': {
        'class': 'Engine',
        'library': 'pages.wizard.rhv.engine',
    },
    'RHV.Hypervisor': {
        'class': 'Hypervisor',
        'library': 'pages.wizard.rhv.hypervisor',
    },
    'RHV.Engine/Hypervisor': {
        'class': 'Hypervisor',
        'library': 'pages.wizard.rhv.hypervisor',
    },
    'RHV.Configuration': {
        'class': 'Configuration',
        'library': 'pages.wizard.rhv.configuration',
    },
    'RHV.Storage': {
        'class': 'Storage',
        'library': 'pages.wizard.rhv.storage',
    },
    'OpenShift.Master/Nodes': {
        'class': 'Nodes',
        'library': 'pages.wizard.openshift.nodes',
    },
    'OpenShift.Configuration': {
        'class': 'Configuration',
        'library': 'pages.wizard.openshift.configuration',
    },
    'RHOSP.Detect Undercloud': {
        'class': 'DetectUndercloud',
        'library': 'pages.wizard.openstack.detect_undercloud',
    },
    'RHOSP.Register Nodes': {
        'class': 'RegisterNodes',
        'library': 'pages.wizard.openstack.register_nodes',
    },
    'RHOSP.Assign Nodes': {
        'class': 'AssignNodes',
        'library': 'pages.wizard.openstack.assign_nodes',
    },
    'RHOSP.Configure Overcloud': {
        'class': 'ConfigureOvercloud',
        'library': 'pages.wizard.openstack.configure_overcloud',
    },
    'CloudForms.Installation Location': {
        'class': 'InstallationLocation',
        'library': 'pages.wizard.cloudforms.installation_location',
    },
    'CloudForms.Configuration': {
        'class': 'Configuration',
        'library': 'pages.wizard.cloudforms.configuration',
    },
    'Subscriptions.Content Provider': {
        'class': 'ContentProviderPage',
        'library': 'pages.wizard.subscriptions.content_provider',
    },
    'Subscriptions.Subscription Management Application': {
        'class': 'SubscriptionManagement',
        'library': 'pages.wizard.subscriptions.subscription_management',
    },
    'Subscriptions.Add Subscriptions': {
        'class': 'AddSubscriptions',
        'library': 'pages.wizard.subscriptions.add_subscriptions',
    },
    'Subscriptions.Review Subscriptions': {
        'class': 'ReviewSubscriptions',
        'library': 'pages.wizard.subscriptions.review_subscriptions',
    },
    'Review.Installation Review': {
        'class': 'InstallationReview',
        'library': 'pages.wizard.review.installation_review',
    },
    'Review.Installation Progress': {
        'class': 'InstallationProgress',
        'library': 'pages.wizard.review.installation_progress',
    },
    'Review.Installation Summary': {
        'class': 'InstallationSummary',
        'library': 'pages.wizard.review.installation_summary',
    },
}


class TaskStepBar():
    """
    This class provides navigation of each deployment's tasks
    steps.   These task steps are displayed as vertical set of
    steps on the side of each deployment wizard's page.  For instance
    in the satellite deployment step you might have

        1A. Deployment Name
        1B. Update Availability
        1C. Insights

    Via this class you may request the name of the class of the
    first node before or after the active state, or of the active state.

    ABBREVIATIONS:

        tsb - Task Step Bar
        dsb - Deployment Step Bar
    """
    def __init__(self, base_url, selenium):
        self.base_url = base_url
        self.selenium = selenium
        self.deployment_step_bar = DeploymentStepBar(
            base_url=self.base_url,
            selenium=self.selenium
        )

    # locators:
    _tsb_loc = (By.XPATH, '//ul[contains(@class, "nav-stacked")]')
    _tsb_steps_loc = (By.XPATH, "{}/li".format(_tsb_loc[1]))
    _tsb_active_step_loc = (
        By.XPATH,
        '{}[contains(@class, "active")]'.format(_tsb_steps_loc[1])
    )
    _tsb_after_active_step_loc = (
        By.XPATH,
        '{}/following-sibling::li[1]'.format(_tsb_active_step_loc[1]),
    )
    _tsb_before_active_step_loc = (
        By.XPATH,
        '{}/preceding-sibling::li[1]'.format(_tsb_active_step_loc[1]),
    )

    # properties
    @property
    def tsb(self):
        return self.selenium.find_element(*self._tsb_loc)

    @property
    def tsb_steps(self):
        return self.selenium.find_elements(*self._tsb_steps_loc)

    @property
    def tsb_active_step(self):
        return self.selenium.find_element(*self._tsb_active_step_loc)

    @property
    def tsb_after_active_step(self):
        return self.selenium.find_element(*self._tsb_after_active_step_loc)

    @property
    def tsb_before_active_step(self):
        return self.selenium.find_element(*self._tsb_before_active_step_loc)

    def number_of_steps(self):
        steps = self.tsb_steps
        return len(steps)

    def get_name_of_step(self, step):
        """
            The text of a step will be preceded by the number of
            the deployment task, and the letter of the task step
            followed by a period, so for instance:

                1A. Deployment Name

            We will strip this off and return just the name of the
            step.

            XXX: I would have preferred to use a posix character
                 class for A-Z, but apparently the re library does
                 not support posix character classes.
        """
        return re.sub(r'^\d+[A-Z]\.\s+', '', step.text)

    def get_number_of_step(self, step):
        alpha_index = re.sub(r'^\d+([A-Z])\.\s+.*', r'\1', step.text)
        number_index = ord(alpha_index) - ord('A') + 1
        return number_index

    def get_step_by_number(self, index):
        steps = self.tsb_steps
        return steps[index - 1]

    def get_current_step(self):
        return self.tsb_active_step

    def get_next_step(self):
        active_step = self.tsb_active_step
        number_of_step = self.get_number_of_step(active_step)
        number_of_steps = self.number_of_steps()
        if number_of_step == number_of_steps:
            return None
        return self.tsb_after_active_step

    def get_prev_step(self):
        active_step = self.tsb_active_step
        number_of_step = self.get_number_of_step(active_step)
        if number_of_step == 1:
            return None
        return self.tsb_before_active_step

    def get_page(self, direction='NEXT'):
        """
        This is the most important method of this
        class, as it allows you to request the page object
        that is either the last page object of the previous
        step or the first page object of the next
        step.

        Arguments:  direction - can be NEXT, PREV, or CURRENT

        """
        if direction == 'NEXT':
            step = self.get_next_step()
        elif direction == 'PREV':
            step = self.get_prev_step()
        elif direction == 'CURRENT':
            step = self.get_current_step()
        else:
            raise NameError('Invalid direction: {}'.format(direction))

        # If we would navigate past the current list of tasks
        # then we need to your the DeploymentStepBar navigator:
        if step is None:
            return self.deployment_step_bar.get_page(direction)

        # We are within our list, so let's continue on.
        #
        # Pull the class and library path based on the direction
        # that was requested.  We will build a fully qualified
        # step name from the current deployment step name and the
        # task step name to do our lookup.
        step_name = self.get_name_of_step(step)
        deployment_step_name = self.deployment_step_bar.get_name_of_step(
            self.deployment_step_bar.dsb_active_step
        )
        fully_qualified_step_name = "{}.{}".format(
            deployment_step_name,
            step_name
        )
        class_name = _step_to_page_map[fully_qualified_step_name]['class']
        library_name = _step_to_page_map[fully_qualified_step_name]['library']

        # import the library if necessary and instantiate an
        # instance of the class:
        page_object_module = __import__(library_name, fromlist=[class_name])
        page_object_class = getattr(page_object_module, class_name)
        instance = page_object_class(
            base_url=self.base_url,
            selenium=self.selenium
        )
        return instance

    def get_next_page(self):
        return self.get_page(direction='NEXT')

    def get_prev_page(self):
        return self.get_page(direction='PREV')

    def get_current_page(self):
        return self.get_page(direction='CURRENT')
