from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.qci_page import QCIPage


class SelectProductsPage(QCIPage):
    _page_title = "QuickStart Cloud Installer"
    _rhv_checkbox_locator = (By.XPATH, "//span[@id='is_rhev']/div/input")
    _openstack_checkbox_locator = (By.XPATH,
                                   "//span[@id='is_openstack']/div/input")
    _cloudforms_checkbox_locator = (By.XPATH,
                                    "//span[@id='is_cloudforms']/div/input")
    _openshift_checkbox_locator = (By.XPATH,
                                   "//span[@id='is_openshift']/div/input")
    # This is the "To deploy the selected products, you will need:" part of
    # the Product Selection screen
    _requirement_block_locator = (By.XPATH, "//div[@class='req-block']")
    _rhv_i_icon_locator = (By.XPATH, "//span[@id='is_rhev']/div/div/span[2]")
    _openstack_i_icon_locator = (By.XPATH,
                                 "//span[@id='is_openstack']/div/div/span[2]")
    _cloudforms_i_icon_locator = (By.XPATH,
                                  "//span[@id='is_cloudforms']/div/div/span[2]")
    _openshift_i_icon_locator = (By.XPATH,
                                 "//span[@id='is_openshift']/div/div/span[2]")
    _requirement_download_locator = (By.XPATH,
                                 "//div[@class='download-reqs']/a")

    @property
    def rhv_checkbox(self):
        return self.selenium.find_element(*self._rhv_checkbox_locator)

    @property
    def openstack_checkbox(self):
        return self.selenium.find_element(*self._openstack_checkbox_locator)

    @property
    def cloudforms_checkbox(self):
        return self.selenium.find_element(*self._cloudforms_checkbox_locator)

    @property
    def openshift_checkbox(self):
        return self.selenium.find_element(*self._openshift_checkbox_locator)

    @property
    def requirement_block(self):
        return self.selenium.find_element(*self._requirement_block_locator)

    @property
    def rhv_i_icon(self):
        return self.selenium.find_element(*self._rhv_i_icon_locator)

    @property
    def openstack_i_icon(self):
        return self.selenium.find_element(*self._openstack_i_icon_locator)

    @property
    def cloudforms_i_icon(self):
        return self.selenium.find_element(*self._cloudforms_i_icon_locator)

    @property
    def openshift_i_icon(self):
        return self.selenium.find_element(*self._openshift_i_icon_locator)

    @property
    def requirement_download(self):
        return self.selenium.find_element(*self._requirement_download_locator)

    # Actions
    def click_rhv(self):
        return self.rhv_checkbox.click()

    def click_openstack(self):
        return self.openstack_checkbox.click()

    def click_cloudforms(self):
        return self.cloudforms_checkbox.click()

    def click_openshift(self):
        return self.openshift_checkbox.click()

    def select_products(self, products):
        if 'rhv' in products and not self.rhv_checkbox.is_selected():
            self.click_rhv()
        if 'osp' in products and not self.openstack_checkbox.is_selected():
            self.click_openstack()
        if 'cfme' in products and not self.cloudforms_checkbox.is_selected():
            self.click_cloudforms()
        if 'ocp' in products and not self.openshift_checkbox.is_selected():
            self.click_openshift()

    def unselect_products(self, products):
        if 'rhv' in products and self.rhv_checkbox.is_selected():
            self.click_rhv()
        if 'osp' in products and self.openstack_checkbox.is_selected():
            self.click_openstack()
        if 'cfme' in products and self.cloudforms_checkbox.is_selected():
            self.click_cloudforms()
        if 'ocp' in products and self.openshift_checkbox.is_selected():
            self.click_openshift()

    def get_requirements(self, product):
        # Requires all the products selected.
        self.select_products(['rhv', 'osp', 'cfme', 'ocp'])

        # reqs[0] = General
        # reqs[1] = RHV
        # reqs[2] = OSP
        # reqs[3] = CFME
        # reqs[4] = OCP
        # reqs[5] = Disconnected
        reqs = self.requirement_block.find_elements_by_tag_name('div')

        dct = {
            'general': reqs[0].text,
            'rhv': reqs[1].text,
            'osp': reqs[2].text,
            'cfme': reqs[3].text,
            'ocp': reqs[4].text,
            'disconnected': reqs[5].text
        }

        return dct[product]


    def i_icon_hover_text(self, div_id):
        return self.selenium.find_element(By.XPATH,
                                          "//div[@id='{}']".format(div_id))

    def _product_icon(self, product):
        dct = {
            'rhv': self.rhv_i_icon,
            'osp': self.openstack_i_icon,
            'cfme': self.cloudforms_i_icon,
            'ocp': self.openshift_i_icon
        }
        return dct[product]

    # Note: if you get 'Element is not clickable' error when using this,
    # it's most probably because another tooltip is already covering
    # the area of the 'i' icon you want to click.
    # Example:
    # First you get the text on the osp tooltip
    # Then you want to get the rhv tooltip, but that is covered by
    # the osp tooltip that is still being displayed.
    # Solution would be to move the cursor away or to click anywhere
    # on the page to make the tooltip go away.
    def get_i_icon_text(self, product):
        self._product_icon(product).click()
        div_id = self._product_icon(product).get_attribute('aria-describedby')
        return self.i_icon_hover_text(div_id).text

    # Navigation Buttons.
    # We need to override base's click_next(), click_back() functions
    # as they all ultimately use the task step bar that does not exist
    # on this page.
    def click_next(self):
        from pages.wizard.satellite.deployment_name import DeploymentName
        self.navigation_buttons.next_btn.click()
        return DeploymentName(self.base_url, self.selenium)

    # there is no back button on this page:
    def click_back(self):
        return None

    @property
    def is_the_current_page(self):
        WebDriverWait(self.selenium, self.timeout).until(
            EC.visibility_of(self.rhv_checkbox),
            "Expected element not present on Select Products Page")
        return True

    def cancel_deployment(self):
        self.click_cancel()
        from pages.deployments import DeploymentsPage
        return DeploymentsPage(self.base_url, self.selenium)
