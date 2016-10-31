from selenium.webdriver.common.by import By
from pages.base import Base


class SubscriptionManagement(Base):

    # locators
    _new_sma_button_loc = (By.XPATH,
                           '//button[@data-qci="register-new-satellite"]')
    _sma_name_field_loc = (By.XPATH,
                           '//input[@id="new-satellite-name"]')
    _submit_new_sma_butt_loc = (By.XPATH,
                                '//button[@data-qci="submit-new-satellite"]')
    _sma_radio_loc = (By.XPATH,
                      '//input[@type="radio"]')

    # elements
    @property
    def new_sma_button(self):
        return self.selenium.find_element(*self._new_sma_button_loc)

    @property
    def new_sma_name_field(self):
        return self.selenium.find_element(*self._sma_name_field_loc)

    @property
    def new_sma_submit_button(self):
        return self.selenium.find_element(*self._submit_new_sma_butt_loc)

    @property
    def sma_radio_buttons(self):
        return self.selenium.find_elements(*self._sma_radio_loc)

    # actions
    def click_new_sma(self):
        """ Click the New Subscription Management Application button"""
        return self.new_sma_button.click()

    def set_new_sma_name(self, name):
        """ Enter the name in the name field for the new SMA"""
        self.new_sma_name_field.clear()
        self.new_sma_name_field.send_keys(name)

    def click_submit_new_sma(self):
        return self.new_sma_submit_button.click()

    def click_sma_radio_by_uuid(self, uuid):
        """ Click the radio button for the SMA with the specified uuid """
        self.wait_for_ajax()
        for sat in self.sma_radio_buttons:
            if uuid in sat.get_attribute('value'):
                # scroll to the element
                self.scroll_to_element(sat)
                return sat.click()
        else:
            raise Exception("No SMA found with uuid: {}".format(uuid))

    def click_sma_radio(self, name):
        """ Click the radio button for the SMA with the specified name """
        self.wait_for_ajax()
        for sat in self.sma_radio_buttons:
            if name in sat.get_attribute('data-qci'):
                # scroll to the element
                self.scroll_to_element(sat)
                return sat.click()
        else:
            raise Exception("No SMA found with name: {}".format(name))
