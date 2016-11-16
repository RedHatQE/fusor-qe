from selenium.webdriver.common.by import By
from pages.qci_page import QCIPage


class AddSubscriptions(QCIPage):

    # locators
    _subs_row_loc = (By.XPATH,
                     '//input[@name="isSelectedSubscription"]/../..')
    _checkbox_loc = (By.XPATH, './/input[@name="isSelectedSubscription"]')
    _quantity_loc = (By.XPATH, './/input[@name="qtyToAttach"]')

    # elements

    @property
    def subscription_rows(self):
        return self.selenium.find_elements(*self._subs_row_loc)

    # actions

    def add_subscription(self, contract, qty):
        """ Adds a subscription (identified by contract #) with the quantity
        specified"""
        for sub in self.subscription_rows:
            cells = sub.find_elements_by_tag_name('td')
            if cells[2].text == str(contract):
                sub.find_element(*self._checkbox_loc).click()
                sub.find_element(*self._quantity_loc).clear()
                sub.find_element(*self._quantity_loc).send_keys(str(qty))
                break
