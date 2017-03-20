from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from qci_page import QCIPage


class DeploymentsPage(QCIPage):
    _page_title = "QuickStart Cloud Installer"

    # Locators
    _search_box_locator = (By.XPATH, '//input[contains(@class, "filter-input")]')
    _search_btn_locator = (By.XPATH, '//button[contains(.,"Search")]')
    _new_deploy_btn_locator = (By.XPATH,
                               '//div[contains(@class, "new-deployment-button")]')
    _deployment_locator = (By.XPATH, '//tr[contains(@class, "deployment-row")]//a[contains(., "{}")]')
    _deployments_locator = (By.XPATH, '//tr[contains(@class, "deployment-row")]')
    _spinner_locator = (By.CLASS_NAME, 'spinner-md')
    _rm_deployment_confirm_locator = (By.XPATH, '//button[contains(., "Delete Deployment")]')

    # elements
    @property
    def search_box(self):
        return self.selenium.find_element(*self._search_box_locator)

    @property
    def search_button(self):
        return self.selenium.find_element(*self._search_btn_locator)

    @property
    def new_deployment_button(self):
        return self.selenium.find_element(*self._new_deploy_btn_locator)

    @property
    def deployment(self, name):
        strategy, loc = self._deployment_locator
        return self.selenium.find_element(strategy, loc.format(name))

    @property
    def deployments(self):
        return self.selenium.find_elements(*self._deployments_locator)

    @property
    def is_the_current_page(self):
        WebDriverWait(self.selenium, self.timeout).until(
            EC.visibility_of(self.new_deployment_button),
            "Could not find expected element for Deployments Page")
        return True

    @property
    def rm_deployment_confirm_btn(self):
        return self.selenium.find_element(*self._rm_deployment_confirm_locator)

    # actions
    def create_new_deployment(self):
        self.new_deployment_button.click()
        from pages.wizard.product_selection import SelectProductsPage
        return SelectProductsPage(self.base_url, self.selenium)

    def clear_search(self):
        self.search_box.clear()

    def delete_deployment(self, name):
        deployment = self.get_deployment(name)
        if deployment is None:
            return

        # Now get the web element for the delete button of this deployment
        # record:
        delete_btn = deployment.find_element_by_css_selector('.btn-danger')
        delete_btn.click()

        # Clicking the delete button will bring up a modal dialogue to confirm
        self.rm_deployment_confirm_btn.click()


    # TODO: We should instead of handing back a web element,  hand back
    #       a simple list of dictionaries of the deployment records.
    def get_deployment(self, name):
        # 1) Get list of deployments, this will actually be a list of the tr web
        #    elements in the deployments table.
        deployments = self.deployments

        # 2) Iterate over the list of deployments and see if the specified name exists.
        needle = None
        for deployment in deployments:
            # 3) Get the text from the first column (that is the deployment name):
            q_dep_name = deployment.find_elements_by_css_selector('td')[0].text

            # 4) See if we found the deployment:
            if q_dep_name == name:
                needle = deployment
                break

        return needle

    def search_deployments(self, query):
        '''
        Filters deployments using the provided query and returns a list of elements of the results
        Note this is useful for testing the actual filter interface on the page, as it will exercise
        '''
        self.search_box.clear()
        self.search_box.send_keys(query)
        self.wait_until_element_is_not_visible(self._spinner_locator)
        return self.deployments


