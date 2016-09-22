import re
from selenium.webdriver.common.by import By

# XXX: Still need to fill this out completely.
# Maps deployment steps to their first and last page.
# In particular it allows one to figure out what library
# and class is used to implement the page object for a
# given page.
_step_to_page_map = {
    'Satellite': {
        'first': {
            'class': 'DeploymentName',
            'library': 'pages.wizard.satellite.deployment_name',
        },
        'last': {
            'class': 'Insights',
            'library': 'pages.wizard.satellite.insights',
        },
    },
    'RHV': {
        'first': {
            'class': 'SetupType',
            'library': 'pages.wizard.rhev.setup_type',
        },
        'last': {
            'class': 'Storage',
            'library': 'pages.wizard.rhev.storage',
        },
    },
    'RHOSP': {
        'first': {
            'class': 'DetectUnder',
            'library': 'pages.wizard.openstack.detect_undercloud',
        },
        'last': {
            'class': 'ConfigureOvercloud',
            'library': 'pages.wizard.openstack.configure_overcloud',
        },
    },
    'OpenShift': {
        'first': {
            'class': '',
            'library': '',
        },
        'last': {
            'class': '',
            'library': '',
        },
    },
    'CloudForms': {
        'first': {
            'class': 'InstallationLocation',
            'library': 'pages.wizard.cloudforms.installation_location',
        },
        'last': {
            'class': 'Configuration',
            'library': 'pages.wizard.cloudforms.configuration',
        },
    },
    'Subscriptions': {
        'first': {
            'class': 'ContentProviderPage',
            'library': 'pages.wizard.subscriptions.content_provider',
        },
        'last': {
            'class': 'ReviewSubscriptions',
            'library': 'pages.wizard.subscriptions.review_subscriptions',
        },
    },
    'Review': {
        'first': {
            'class': 'InstallationReview',
            'library': 'pages.wizard.review.installation_review',
        },
        'last': {
            'class': 'InstallationSummary',
            'library': 'pages.wizard.review.installation_summary',
        },
    },
}


class DeploymentStepBar():
    """
    This class provides navigation of the deployment
    wizards major deployment states.   These deployment
    states are displayed as the QCI Deployment Step Bar at
    the top of the QCI Deployment Wizard after the products
    to deploy have been chosen.   For instance when
    deploying RHEV and CloudForms the QCI Deployment Step Bar
    may look like:

        1. Satellite 2. RHEV  3. CloudForms 4. Subscriptions 5. Review
        1. Satellite 2. RHOSP 3. CloudForms 4. Subscriptions 5. Review
        1. Satellite 2. RHEV 3. RHOSP 4. CloudForms 5. Subscriptions 6. Review
        1. Satellite 2. RHEV 3. RHOSP 4. OpenShift 5. CloudForms 6. Subscriptions 7. Review
        1. Satellite 2. RHEV 3. OpenShift 4. Subscriptions 5. Review

    These are not all permutations, just some samples.

    Via this class you may request the name of the class of the
    first node before or after the active state.

    ABBREVIATIONS:

        DSB - Deployment Step Bar
    """
    def __init__(self, base_url, selenium):
        self.base_url = base_url
        self.selenium = selenium

    # locators:
    _DSB_loc = (By.XPATH, '//ul[@class="rhci-steps"]')
    _DSB_steps_loc = (By.XPATH, "{}/li".format(_DSB_loc[1]))
    _DSB_active_step_loc = (
        By.XPATH,
        '{}[contains(@class, "active")]'.format(_DSB_steps_loc[1])
    )
    _DSB_after_active_step_loc = (
        By.XPATH,
        '{}/following-sibling::li[1]'.format(_DSB_active_step_loc[1]),
    )
    _DSB_before_active_step_loc = (
        By.XPATH,
        '{}/preceding-sibling::li[1]'.format(_DSB_active_step_loc[1]),
    )

    # properties
    @property
    def DSB(self):
        return self.selenium.find_element(*self._DSB_loc)

    @property
    def DSB_steps(self):
        return self.selenium.find_elements(*self._DSB_steps_loc)

    @property
    def DSB_active_step(self):
        return self.selenium.find_element(*self._DSB_active_step_loc)

    @property
    def DSB_after_active_step(self):
        return self.selenium.find_element(*self._DSB_after_active_step_loc)

    @property
    def DSB_before_active_step(self):
        return self.selenium.find_element(*self._DSB_before_active_step_loc)

    def number_of_steps(self):
        steps = self.DSB_steps
        return len(steps)

    def get_name_of_step(self, step):
        return re.sub('^\d+\.\s+', '', step.text)

    def get_step_by_number(self, index):
        steps = self.DSB_steps
        return steps[index - 1]

    def get_next_step(self):
        return self.DSB_after_active_step

    def get_prev_step(self):
        return self.DSB_before_active_step

    def get_page(self, direction='NEXT'):
        """
        This is the most important method of this
        class, as it allows you to request the page object
        that is either the last page object of the previous
        deployment step or the first page object of the next
        deployment step.   This enables the next button implementations
        of our page objects to navigate between deployment steps.

        Arguments:  direction - can be NEXT or PREV

        """
        if direction == 'NEXT':
            menu_pos = 'first'
            step = self.get_next_step()
        elif direction == 'PREV':
            menu_pos = 'last'
            step = self.get_prev_step()
        else:
            raise NameError('Invalid direction: {}'.format(direction))

        # Pull the class and library path based on the direction
        # that was requested
        step_name = self.get_name_of_step(step)
        class_name = _step_to_page_map[step_name][menu_pos]['class']
        library_name = _step_to_page_map[step_name][menu_pos]['library']

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
