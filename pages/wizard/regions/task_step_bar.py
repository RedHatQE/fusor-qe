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
        'library': 'pages.wizard.rhev.setup_type',
    },
    'RHV.Engine': {
        'class': 'Engine',
        'library': 'pages.wizard.rhev.engine',
    },
    'RHV.Hypervisor': {
        'class': 'Hypervisor',
        'library': 'pages.wizard.rhev.hypervisor',
    },
    'RHV.Configuration': {
        'class': 'Configuration',
        'library': 'pages.wizard.rhev.configuration',
    },
    'RHV.Storage': {
        'class': 'Storage',
        'library': 'pages.wizard.rhev.storage',
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

        TSB - Task Step Bar
        DSB - Deployment Step Bar
    """
    def __init__(self, base_url, selenium):
        self.base_url = base_url
        self.selenium = selenium
        self.deployment_step_bar = DeploymentStepBar(
            base_url=self.base_url,
            selenium=self.selenium
        )

    # locators:
    _TSB_loc = (By.XPATH, '//ul[contains(@class, "nav-stacked")]')
    _TSB_steps_loc = (By.XPATH, "{}/li".format(_TSB_loc[1]))
    _TSB_active_step_loc = (
        By.XPATH,
        '{}[contains(@class, "active")]'.format(_TSB_steps_loc[1])
    )
    _TSB_after_active_step_loc = (
        By.XPATH,
        '{}/following-sibling::li[1]'.format(_TSB_active_step_loc[1]),
    )
    _TSB_before_active_step_loc = (
        By.XPATH,
        '{}/preceding-sibling::li[1]'.format(_TSB_active_step_loc[1]),
    )

    # properties
    @property
    def TSB(self):
        return self.selenium.find_element(*self._TSB_loc)

    @property
    def TSB_steps(self):
        return self.selenium.find_elements(*self._TSB_steps_loc)

    @property
    def TSB_active_step(self):
        return self.selenium.find_element(*self._TSB_active_step_loc)

    @property
    def TSB_after_active_step(self):
        return self.selenium.find_element(*self._TSB_after_active_step_loc)

    @property
    def TSB_before_active_step(self):
        return self.selenium.find_element(*self._TSB_before_active_step_loc)

    def number_of_steps(self):
        steps = self.TSB_steps
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
        alphaIndex = re.sub(r'^\d+([A-Z])\.\s+.*', r'\1', step.text)
        numberIndex = ord(alphaIndex) - ord('A') + 1
        return numberIndex

    def get_step_by_number(self, index):
        steps = self.TSB_steps
        return steps[index - 1]

    def get_current_step(self):
        return self.TSB_active_step

    def get_next_step(self):
        active_step = self.TSB_active_step
        number_of_step = self.get_number_of_step(active_step)
        number_of_steps = self.number_of_steps()
        if number_of_step == number_of_steps:
            return None
        return self.TSB_after_active_step

    def get_prev_step(self):
        active_step = self.TSB_active_step
        number_of_step = self.get_number_of_step(active_step)
        if number_of_step == 1:
            return None
        return self.TSB_before_active_step

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
        if step == None:
            return self.deployment_step_bar.get_page(direction)


        # We are within our list, so let's continue on.
        #
        # Pull the class and library path based on the direction
        # that was requested.  We will build a fully qualified
        # step name from the current deployment step name and the
        # task step name to do our lookup.
        step_name = self.get_name_of_step(step)
        deployment_step_name = self.deployment_step_bar.get_name_of_step(
            self.deployment_step_bar.DSB_active_step
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
