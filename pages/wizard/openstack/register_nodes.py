# This page is really pages within a page.   I've tried through comments
# to show the elements that are part of each page.   But basically you have
# the main page where you click register.  Once you do  a modal frame popup
# appear.   This frame allows you to register all info about the
# system you need to use to scan for overcloud systems (so for instance
# the information on your libvirt host if you are using the PXE+SSH driver).
# If you select, upload CSV, the modal changes to an upload CSV screen.
# If you click the modal's next button it changes the modal to the
# Node-autodetection screen.  From there clicking Register will take you
# back to the original screen, where you can then click next to go to
# the Assign Nodes page.
#
# The following comments help divide the code into the particular sections
# they support:
#
#   <<< MAIN SCREEN >>>
#   <<< Register Nodes >>>
#   <<< Browse CSV Screen >>>
#   <<< Node Auto Detection >>>
#   <<< Modal Navigation Buttons >>>
#
# Note, the modal navigation buttons in some cases may be found on
# multiple modal frames.
#
# XXX:  It might be good to split this into multiple files somehow.
# XXX:  The code to handle the  table in the Node Auto Detection modal
#       might be handled better by a library to represent the table and
#       it's records.   The fact that we call multiple routines with
#       row_id almost cries out for the existence of an object.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pages.qci_page import QCIPage


class RegisterNodes(QCIPage):
    _page_title = "QuickStart Cloud Installer"

    # locators
    # <<< MAIN SCREEN >>>
    _register_nodes_loc = (
        By.XPATH,
        "//button[@id = 'register-nodes-button']"
    )

    # <<< Register Nodes >>>
    _ip_address_loc = (By.XPATH, "//input[@id = 'newNodeIpAddressInput']")
    _driver_loc = (By.XPATH, "//select[@id = 'newNodeDriverInput']")
    _username_loc = (By.XPATH, "//input[@id = 'newNodeIpmiUserInput']")
    _password_loc = (By.XPATH, "//input[@id = 'newNodePasswordInput']")
    #
    # The autodetect "widget" is kind of bizarre (translate I don't really
    # understand it.  If you try to click on the actual radio button that
    # represents it, it will never changes.   However if you click on the
    # span tag that that encloses it, it will change.   However if you want
    # to know if autodetect is selected or not you have to get that from
    # the radio button.   So that is why there are two locaters here.
    _autodetect_loc = (By.XPATH, "//span[@class='bootstrap-switch-label']")
    _autodetect_radio_btn_loc = (
        By.XPATH,
        "//div[@class = 'bootstrap-switch-container']/input"
    )
    _mac_addresses_loc = (By.XPATH, "//textarea[@id = 'newNodeMacAddressManualInput']")
    _ssh_vendor_loc = (By.XPATH, "//select[@id = 'newNodeVendorInputSsh']")
    _ipmi_vendor_loc = (By.XPATH, "//select[@id = 'newNodeVendorInputIpmi']")
    _upload_csv_loc = (By.XPATH, "//input[@value = 'csv_upload']")

    # <<< Browse CSV Screen >>>
    _browse_csv_loc = (By.XPATH, "//input[@id = 'csvUploadInput']")

    # <<< Node Auto Detection >>>
    _rescan_loc = (By.XPATH, "//a[contains(., 'Re-scan')]")
    _node_list_loc = (By.XPATH, "//div[@class = 'new-node-detect-list']")
    _node_list_rows_loc = (
        By.XPATH,
        "{}/div".format(
            _node_list_loc[1]
        )
    )
    # Note the @id parameter on the dev element.   This must be
    # filled out later by code below with specific ID values.
    # The next two locators use this locator, and thus will need the
    # ID parameter for the div element to be provided.
    _specific_node_list_row_loc = (
        By.XPATH,
        "{}/div[@id = '{{}}']/form[contains(@class, 'new-node-detect-form')]".format(
            _node_list_loc[1]
        )
    )
    _specific_node_list_row_checkbox_loc = (
        By.XPATH,
        "{}//input[@name = 'autoDetectedNodeSelected']".format(
            _specific_node_list_row_loc[1]
        )
    )
    # XXX: Wanted the select to be identified uniquely but I couldn't really
    #      find anything about it that was unique.   If they ever add
    #      a second column with a select then we will have to revisit this.
    _specific_node_list_row_select_interface_loc = (
        By.XPATH,
        "{}//select".format(
            _specific_node_list_row_loc[1]
        )
    )
    _specific_node_list_row_name_loc = (
        By.XPATH,
        "{}//span[contains(@class,  'new-node-detect-hostname')]".format(
            _specific_node_list_row_loc[1]
        )

    )

    # <<< Modal Navigation Buttons >>>
    _register_loc = (By.XPATH, "//button[@id = 'newNodeSubmitButton']")
    _inner_cancel_loc = (
        By.XPATH,
        "//button[@id = 'newNodeCancelButton']"
    )
    _inner_next_loc = (
        By.XPATH,
        "//button[@id = 'detectNodeSubmitButton']"
    )
    _inner_back_loc = (
        By.XPATH,
        "//button[@id = 'newNodeBackButton']"
    )

    # properties
    # <<< MAIN SCREEN >>>
    @property
    def register_nodes(self):
        return self.selenium.find_element(*self._register_nodes_loc)

    # <<< Register Nodes >>>
    @property
    def ip_address(self):
        return self.selenium.find_element(*self._ip_address_loc)

    @property
    def driver(self):
        return Select(self.selenium.find_element(*self._driver_loc))

    @property
    def username(self):
        return self.selenium.find_element(*self._username_loc)

    @property
    def password(self):
        return self.selenium.find_element(*self._password_loc)

    @property
    def autodetect(self):
        return self.selenium.find_element(*self._autodetect_loc)

    @property
    def autodetect_radio_btn(self):
        return self.selenium.find_element(*self._autodetect_radio_btn_loc)

    @property
    def ssh_vendor(self):
        return Select(self.selenium.find_element(*self._ssh_vendor_loc))

    @property
    def ipmi_vendor(self):
        return Select(self.selenium.find_element(*self._ipmi_vendor_loc))

    @property
    def mac_addresses(self):
        return self.selenium.find_element(*self._mac_addresses_loc)

    @property
    def upload_csv(self):
        return self.selenium.find_element(*self._upload_csv_loc)

    # <<< Browse CSV Screen >>>
    @property
    def browse_csv(self):
        return self.selenium.find_element(*self._browse_csv_loc)

    # <<< Node Auto Detection >>>
    @property
    def rescan(self):
        return self.selenium.find_element(*self._rescan_loc)

    @property
    def node_list_rows(self):
        return self.selenium.find_elements(*self._node_list_rows_loc)

    # <<< Modal Navigation Buttons >>>
    @property
    def register(self):
        return self.selenium.find_element(*self._register_loc)

    @property
    def inner_cancel(self):
        return self.selenium.find_element(*self._inner_cancel_loc)

    @property
    def inner_next(self):
        return self.selenium.find_element(*self._inner_next_loc)

    @property
    def inner_back(self):
        return self.selenium.find_element(*self._inner_back_loc)

    # actions
    # <<< MAIN SCREEN >>>
    def click_register_nodes(self):
        self.register_nodes.click()

    # <<< Register Nodes >>>
    def set_ip_address(self, text):
        self.ip_address.clear()
        self.ip_address.send_keys(text)

    def set_username(self, text):
        self.username.clear()
        self.username.send_keys(text)

    def set_password(self, text):
        self.password.click()
        self.password.clear()
        self.password.click()
        self.password.send_keys(text)

    def click_autodetect(self):
        self.autodetect.click()

    def is_autodetect_enabled(self):
        return self.autodetect_radio_btn.is_selected()

    def set_mac_addresses(self, text):
        self.mac_addresses.clear()
        self.mac_addresses.send_keys(text)

    def click_upload_csv(self):
        self.upload_csv.click()

    # <<< Browse CSV Screen >>>
    def set_browse_csv(self, text):
        self.browse_csv.clear()
        self.browse_csv.send_keys(text)

    # <<< Node Auto Detection >>>
    #
    # The work flow here is basically:
    #
    #   - Get the row ID of the node you want based on the name
    #     of the host.  These row ID's are auto-generated ember
    #     ID's so you have to start with this:
    #
    #       row_id = regNodes.node_list_row_id_by_name('bob')
    #
    #   - Select the node list row using that row_id:
    #
    #       regNodes.select_node_list_row(row_id)
    #
    #   - Get the interfaces available for that node using the row_id:
    #
    #       @interfaces = regNodes.node_list_row_get_interfaces(row_id)
    #
    #   - Select the interface you want:
    #
    #       regNodes.node_list_row_select_interface(row_id, interface[1])
    #
    def click_rescan(self):
        self.rescan.click()

    def get_node_name_by_id(self, row_id):
        locator_type = self._specific_node_list_row_name_loc[0]
        locator = self._specific_node_list_row_name_loc[1].format(row_id)
        return self.selenium.find_element(locator_type, locator).text

    def select_node_list_row(self, row_id):
        locator_type = self._specific_node_list_row_checkbox_loc[0]
        locator = self._specific_node_list_row_checkbox_loc[1].format(row_id)
        self.selenium.find_element(locator_type, locator).click()

    def node_list_row_get_interface_select(self, row_id):
        locator_type = self._specific_node_list_row_select_interface_loc[0]
        locator = self._specific_node_list_row_select_interface_loc[1].format(
            row_id
        )
        return Select(self.selenium.find_element(locator_type, locator))

    def node_list_row_get_interfaces(self, row_id):
        selector = self.node_list_row_get_interface_select(row_id)
        macs = []
        for option in selector.options:
            macs.append(option.get_attribute('value'))
        return macs

    def node_list_row_select_interface(self, row_id, mac):
        selector = self.node_list_row_get_interface_select(row_id)
        selector.select_by_value(mac)

    def node_list_row_id_by_name(self, node_name):
        rows = self.node_list_rows
        for row in rows:
            # Get row id so we can lookup the
            # corresponding node name, and see if
            # it matches the one given.
            row_id = row.get_attribute('id')
            cur_node_name = self.get_node_name_by_id(row_id)
            if node_name == cur_node_name:
                return row_id
        return None

    # <<< Modal Navigation Buttons >>>
    def click_register(self):
        self.register.click()

    def click_inner_cancel(self):
        self.inner_cancel.click()

    def click_inner_next(self):
        self.inner_next.click()

    def click_inner_back(self):
        self.inner_back.click()
