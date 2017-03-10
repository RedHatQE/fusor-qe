class RHV(object):
    '''
    This class contains all the config information for a RHV
    deployment.
    '''

    @property
    def cluster_name(self):
        return self.__cluster_name

    @cluster_name.setter
    def cluster_name(self, value):
        self.__cluster_name = value

    @property
    def cpu_type(self):
        return self.__cpu_type

    @cpu_type.setter
    def cpu_type(self, value):
        self.__cpu_type = value

    @property
    def data_center_name(self):
        return self.__data_center_name

    @data_center_name.setter
    def data_center_name(self, value):
        self.__data_center_name = value

    @property
    def data_domain_address(self):
        return self.__data_domain_address

    @data_domain_address.setter
    def data_domain_address(self, value):
        self.__data_domain_address = value

    @property
    def data_domain_name(self):
        return self.__data_domain_name

    @data_domain_name.setter
    def data_domain_name(self, value):
        self.__data_domain_name = value

    @property
    def data_domain_share_path(self):
        return self.__data_domain_share_path

    @data_domain_share_path.setter
    def data_domain_share_path(self, value):
        self.__data_domain_share_path = value

    @property
    def export_domain_address(self):
        return self.__export_domain_address

    @export_domain_address.setter
    def export_domain_address(self, value):
        self.__export_domain_address = value

    @property
    def export_domain_name(self):
        return self.__export_domain_name

    @export_domain_name.setter
    def export_domain_name(self, value):
        self.__export_domain_name = value

    @property
    def export_domain_share_path(self):
        return self.__export_domain_share_path

    @export_domain_share_path.setter
    def export_domain_share_path(self, value):
        self.__export_domain_share_path = value

    @property
    def hypervisor_count(self):
        return self.__hypervisor_count

    @hypervisor_count.setter
    def hypervisor_count(self, value):
        self.__hypervisor_count = value

    @property
    def include(self):
        return self.__include

    @include.setter
    def include(self, value):
        self.__include = value

    @property
    def rhv_setup_type(self):
        return self.__rhv_setup_type

    @rhv_setup_type.setter
    def rhv_setup_type(self, value):
        self.__rhv_setup_type = value

    @property
    def rhvh_hostname(self):
        return self.__rhvh_hostname

    @rhvh_hostname.setter
    def rhvh_hostname(self, value):
        self.__rhvh_hostname = value

    @property
    def rhvh_macs(self):
        return self.__rhvh_macs

    @rhvh_macs.setter
    def rhvh_macs(self, value):
        self.__rhvh_macs = value

    @property
    def rhvm_adminpass(self):
        return self.__rhvm_adminpass

    @rhvm_adminpass.setter
    def rhvm_adminpass(self, value):
        self.__rhvm_adminpass = value

    @property
    def rhvm_engine(self):
        return self.__rhvm_engine

    @rhvm_engine.setter
    def rhvm_engine(self, value):
        self.__rhvm_engine = value

    @property
    def rhvm_hostname(self):
        return self.__rhvm_hostname

    @rhvm_hostname.setter
    def rhvm_hostname(self, value):
        self.__rhvm_hostname = value

    @property
    def rhvm_hypervisors(self):
        return self.__rhvm_hypervisors

    @rhvm_hypervisors.setter
    def rhvm_hypervisors(self, value):
        self.__rhvm_hypervisors = value

    @property
    def rhvm_mac(self):
        return self.__rhvm_mac

    @rhvm_mac.setter
    def rhvm_mac(self, value):
        self.__rhvm_mac = value

    @property
    def storage_type(self):
        return self.__storage_type

    @storage_type.setter
    def storage_type(self, value):
        self.__storage_type = value

    @property
    def selfhosted_domain_name(self):
        return self.__selfhosted_domain_name

    @selfhosted_domain_name.setter
    def selfhosted_domain_name(self, value):
        self.__selfhosted_domain_name = value

    @property
    def selfhosted_domain_address(self):
        return self.__selfhosted_domain_address

    @selfhosted_domain_address.setter
    def selfhosted_domain_address(self, value):
        self.__selfhosted_domain_address = value

    @property
    def selfhosted_domain_share_path(self):
        return self.__selfhosted_domain_share_path

    @selfhosted_domain_share_path.setter
    def selfhosted_domain_share_path(self, value):
        self.__selfhosted_domain_share_path = value

    @property
    def self_hosted_engine_hostname(self):
        return self.__self_hosted_engine_hostname

    @self_hosted_engine_hostname.setter
    def self_hosted_engine_hostname(self, value):
        self.__self_hosted_engine_hostname = value
