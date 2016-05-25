from selenium.webdriver.common.by import By
from pages.base import Base
from pages.wizard.rhev.hosts import Hosts

class Hypervisor(Base):
    _page_title = "QuickStart Cloud Installer"
    _search_box_loc = (By.XPATH, "//input[@placeholder=' Search ...']")
    _refresh_data_loc = (By.XPATH, "//button[contains(.,'Refresh Data')]")
    _naming_scheme_loc = (By.XPATH, "//button[contains(.,'Edit Naming Scheme')]")
    _select_all_loc = (By.XPATH, "//span[@class = 'rhev-select-all']/a")
    _host_table_loc = (By.XPATH, "//div[@class = 'col-lg-9']/table")
    _naming_scheme_cancel_loc = (By.XPATH, \
        "//div[@class = 'modal-footer']/button[contains(., 'Cancel')]")
    _naming_scheme_edit_loc = (By.XPATH, \
        "//div[@class = 'modal-footer']/button[contains(., 'Edit')]")
    _naming_scheme_dropdown_loc = (By.XPATH, "//div[@role = 'button']")
    _naming_scheme_dropwown_search_loc = (By.XPATH, \
        "//div[@class = 'ember-power-select-search']/input")
    _naming_scheme_dropwown_free_loc = (By.XPATH, \
        "//div[@class = 'ember-power-select-search']/../ul/li[contains(., 'Freeform')]")
    _naming_scheme_dropwown_mac_loc = (By.XPATH, \
        "//div[@class = 'ember-power-select-search']/../ul/li[contains(., 'MAC address')]")
    _naming_scheme_dropwown_hyper_loc = (By.XPATH, \
        "//div[@class = 'ember-power-select-search']/../ul/li[contains(., 'hypervisorN')]")
    _naming_scheme_dropwown_custom_loc = (By.XPATH, \
        "//div[@class = 'ember-power-select-search']/../ul/li[contains(., 'Custom scheme')]")
    _naming_scheme_custom_prepend_loc = (By.XPATH, "//div[@class = 'form-group ']/div/input")

    @property
    def search_box(self):
        return self.selenium.find_element(*self._search_box_loc)

    @property
    def refresh_data_button(self):
        return self.selenium.find_element(*self._refresh_data_loc)

    @property
    def naming_scheme_button(self):
        return self.selenium.find_element(*self._naming_scheme_loc)

    @property
    def select_all_link(self):
        return self.selenium.find_element(*self._select_all_loc)

    @property
    def hosts(self):
        return Hosts(self.selenium.find_element(*self._host_table_loc))

    @property
    def naming_scheme_cancel_button(self):
        return self.selenium.find_element(*self._naming_scheme_cancel_loc)

    @property
    def naming_scheme_edit_button(self):
        return self.selenium.find_element(*self._naming_scheme_edit_loc)

    @property
    def naming_scheme_dropdown(self):
        return self.selenium.find_element(*self._naming_scheme_dropdown_loc)

    @property
    def naming_scheme_search_field(self):
        return self.selenium.find_element(*self._naming_scheme_dropwown_search_loc)

    @property
    def naming_scheme_freeform(self):
        return self.selenium.find_element(*self._naming_scheme_dropwown_free_loc)

    @property
    def naming_scheme_mac_address(self):
        return self.selenium.find_element(*self._naming_scheme_dropwown_mac_loc)

    @property
    def naming_scheme_hypervisorn(self):
        return self.selenium.find_element(*self._naming_scheme_dropwown_hyper_loc)

    @property
    def naming_scheme_custom(self):
        return self.selenium.find_element(*self._naming_scheme_dropwown_custom_loc)

    @property
    def naming_scheme_custom_prepend_field(self):
        return self.selenium.find_element(*self._naming_scheme_custom_prepend_loc)

    def search(self, phrase):
        self.search_box.clear()
        self.search_box.send_keys(phrase)

    def click_refresh_data(self):
        self.refresh_data_button.click()

    def click_naming_scheme(self):
        self.naming_scheme_button.click()

    def click_select_all(self):
        self.select_all_link.click()

    def click_naming_scheme_cancel(self):
        self.naming_scheme_cancel_button.click()

    def click_naming_scheme_edit(self):
        self.naming_scheme_edit_button.click()

    def naming_scheme_search(self, phrase):
        self.naming_scheme_search_field.clear()
        self.naming_scheme_search_field.send_keys(phrase)

    def click_naming_scheme_freeform(self):
        self.naming_scheme_freeform.click()

    def click_naming_scheme_mac_address(self):
        self.naming_scheme_mac_address.click()

    def click_naming_scheme_hypervisorn(self):
        self.naming_scheme_hypervisorn.click()

    def click_naming_scheme_custom(self):
        self.naming_scheme_custom.click()

    def naming_scheme_custom_prepend(self, phrase):
        self.naming_scheme_custom_prepend_field.clear()
        self.naming_scheme_custom_prepend_field.send_keys(phrase)

    def choose_naming_scheme_dropdown(self):
        self.naming_scheme_dropdown.click()

