from selenium.webdriver.common.by import By
from pages.base import Base

class Nodes(Base):
    _page_title = "QuickStart Cloud Installer"
    _rhv_radio_loc = (By.XPATH, "//input[@value='RHEV']")
    _master_node_count_loc = (By.XPATH, "//span[@data-qci='master-1']")
    _worker_custom_link_loc = (By.XPATH, "//a[@data-qci='show-custom-worker-nodes']")
    _storage_custom_link_loc = (By.XPATH, "//a[@data-qci='show-custom-storage-size']")
    _custom_edit_loc = (By.XPATH, "//button[contains(., 'Custom Edit')]")
    _finish_editing_loc = (By.XPATH, "//button[contains(., 'Finish Editing')]")
    _master_vcpu_loc = (By.ID, "master-v_cpu")
    _master_ram_loc = (By.ID, "master-ram")
    _master_disk_loc = (By.ID, "master-disk")
    _worker_vcpu_loc = (By.ID, "worker-v_cpu")
    _worker_ram_loc = (By.ID, "worker-ram")
    _worker_disk_loc = (By.ID, "worker-disk")

    @property
    def rhv_radio_button(self):
        return self.selenium.find_element(*self._rhv_radio_loc)

    @property
    def master_node_count(self):
        return self.selenium.find_element(*self._master_node_count_loc)

    def worker_node_count(self, number):
        return self.selenium.find_element(
            By.XPATH, "//span[@data-qci='worker-{}']".format(number)
        )

    @property
    def worker_node_custom(self):
        return self.selenium.find_element(*self._worker_custom_link_loc)

    def additional_storage(self, number):
        return self.selenium.find_element(
            By.XPATH, "//span[@data-qci='storageSize-{}']".format(number)
        )

    @property
    def storage_custom(self):
        return self.selenium.find_element(*self._storage_custom_link_loc)

    @property
    def custom_edit_button(self):
        return self.selenium.find_element(*self._custom_edit_loc)

    @property
    def finish_edditing_button(self):
        return self.selenium.find_element(*self._finish_editing_loc)

    @property
    def master_vcpu(self):
        return self.selenium.find_element(*self._master_vcpu_loc)

    @property
    def master_ram(self):
        return self.selenium.find_element(*self._master_ram_loc)

    @property
    def master_disk(self):
        return self.selenium.find_element(*self._master_disk_loc)

    @property
    def worker_vcpu(self):
        return self.selenium.find_element(*self._worker_vcpu_loc)

    @property
    def worker_ram(self):
        return self.selenium.find_element(*self._worker_ram_loc)

    @property
    def worker_disk(self):
        return self.selenium.find_element(*self._worker_disk_loc)

    def click_rhv(self):
        self.rhv_radio_button.click()

    def click_master_nodes(self):
        self.master_node_count.click()

    def click_worker_nodes(self, number):
        self.worker_node_count(number).click()

    def click_additional_storage(self, number):
        self.additional_storage(number).click()

    def click_worker_node_custom(self):
        self.worker_node_custom.click()

    def click_storage_custom(self):
        self.storage_custom.click()

    def click_custom_edit(self):
        self.custom_edit_button.click()

    def click_finish_edit(self):
        self.finish_edditing_button.click()

    def set_master_vcpu(self, number):
        self.master_vcpu.clear()
        self.master_vcpu.send_keys(number)

    def set_master_ram(self, number):
        self.master_ram.clear()
        self.master_ram.send_keys(number)

    def set_master_disk(self, number):
        self.master_disk.clear()
        self.master_disk.send_keys(number)

    def set_worker_vcpu(self, number):
        self.worker_vcpu.clear()
        self.worker_vcpu.send_keys(number)

    def set_worker_ram(self, number):
        self.worker_ram.clear()
        self.worker_ram.send_keys(number)

    def set_worker_disk(self, number):
        self.worker_disk.clear()
        self.worker_disk.send_keys(number)

