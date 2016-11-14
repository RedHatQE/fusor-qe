from selenium.webdriver.common.by import By
from pages.base import Base


class Configuration(Base):
    _page_title = "QuickStart Cloud Installer"
    _root_password_loc = (By.ID, "rhev-root-password")
    _confirm_root_password_loc = (By.ID, "confirm-rhev-root-password")
    _engine_admin_password_loc = (By.ID, "rhev-engine-admin-password")
    _confirm_engine_admin_password_loc = (By.ID, "confirm-rhev-engine-pdmin-password")
    _data_center_name_loc = (By.ID, "rhev-data-center-name")
    _cluster_name_loc = (By.ID, "rhev-cluster-name")
    _cpu_type_loc = (By.XPATH, "//div[@role = 'button']")
    _cpu_type_search_loc = (By.XPATH, "//div[@class = 'ember-power-select-search']/input")
    _cpu_type_dropdown_items_loc = (By.XPATH,
                                    "//div[@class = 'ember-power-select-search']/../ul/li")

    @property
    def root_password_field(self):
        return self.selenium.find_element(*self._root_password_loc)

    @property
    def confirm_root_password_field(self):
        return self.selenium.find_element(*self._confirm_root_password_loc)

    @property
    def engine_admin_password_field(self):
        return self.selenium.find_element(*self._engine_admin_password_loc)

    @property
    def confirm_engine_admin_password_field(self):
        return self.selenium.find_element(*self._confirm_engine_admin_password_loc)

    @property
    def data_center_name_field(self):
        return self.selenium.find_element(*self._data_center_name_loc)

    @property
    def cluster_name_field(self):
        return self.selenium.find_element(*self._cluster_name_loc)

    @property
    def cpu_type_dropdown(self):
        return self.selenium.find_element(*self._cpu_type_loc)

    @property
    def cpu_type_dropdown_items(self):
        return self.selenium.find_elements(*self._cpu_type_dropdown_items_loc)

    @property
    def cpu_type_search_field(self):
        return self.selenium.find_element(*self._cpu_type_search_loc)

    def set_root_password(self, password):
        self.root_password_field.clear()
        self.root_password_field.send_keys(password)

    def set_confirm_root_password(self, password):
        self.confirm_root_password_field.clear()
        self.confirm_root_password_field.send_keys(password)

    def set_root_passwords(self, password):
        self.set_root_password(password)
        self.set_confirm_root_password(password)

    def set_engine_password(self, password):
        self.engine_admin_password_field.clear()
        self.engine_admin_password_field.send_keys(password)

    def set_confirm_engine_password(self, password):
        self.confirm_engine_admin_password_field.clear()
        self.confirm_engine_admin_password_field.send_keys(password)

    def set_engine_passwords(self, password):
        self.set_engine_password(password)
        self.set_confirm_engine_password(password)

    def set_data_center_name(self, name):
        self.data_center_name_field.clear()
        self.data_center_name_field.send_keys(name)

    def set_cluster_name(self, name):
        self.cluster_name_field.clear()
        self.cluster_name_field.send_keys(name)

    def click_cpu_type_dropdown(self):
        self.cpu_type_dropdown.click()

    def set_cpu_type_search(self, phrase):
        self.cpu_type_search_field.clear()
        self.cpu_type_search_field.send_keys(phrase)

    def set_cpu_type(self, cpu_type):
        from selenium.common.exceptions import StaleElementReferenceException

        self.click_cpu_type_dropdown()
        for item in self.cpu_type_dropdown_items:
            try:
                if str(cpu_type) == str(item.text):
                    item.click()
                    return
            except StaleElementReferenceException:
                pass
        raise NameError("Can't find specified cpu type.")
