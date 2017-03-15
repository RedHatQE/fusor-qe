class OCP(object):
    '''
    This class contains all the config information for an OCP
    deployment.
    '''
    @property
    def ose_address(self):
        return self.__ose_address

    @ose_address.setter
    def ose_address(self, value):
        self.__ose_address = value

    @property
    def subscription(self):
        return self.__subscription

    @subscription.setter
    def subscription(self, value):
        self.__subscription = value

    @property
    def install_loc(self):
        return self.__install_loc

    @install_loc.setter
    def install_loc(self, value):
        self.__install_loc = value

    @property
    def storage_size(self):
        return self.__storage_size

    @storage_size.setter
    def storage_size(self, value):
        self.__storage_size = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def user_password(self):
        return self.__user_password

    @user_password.setter
    def user_password(self, value):
        self.__user_password = value

    @property
    def root_password(self):
        return self.__root_password

    @root_password.setter
    def root_password(self, value):
        self.__root_password = value

    @property
    def master_vcpu(self):
        return self.__master_vcpu

    @master_vcpu.setter
    def master_vcpu(self, value):
        self.__master_vcpu = value

    @property
    def master_ram(self):
        return self.__master_ram

    @master_ram.setter
    def master_ram(self, value):
        self.__master_ram = value

    @property
    def master_disk(self):
        return self.__master_disk

    @master_disk.setter
    def master_disk(self, value):
        self.__master_disk = value

    @property
    def node_vcpu(self):
        return self.__node_vcpu

    @node_vcpu.setter
    def node_vcpu(self, value):
        self.__node_vcpu = value

    @property
    def node_ram(self):
        return self.__node_ram

    @node_ram.setter
    def node_ram(self, value):
        self.__node_ram = value

    @property
    def node_disk(self):
        return self.__node_disk

    @node_disk.setter
    def node_disk(self, value):
        self.__node_disk = value

    @property
    def available_vcpu(self):
        return self.__available_vcpu

    @available_vcpu.setter
    def available_vcpu(self, value):
        self.__available_vcpu = value

    @property
    def available_ram(self):
        return self.__available_ram

    @available_ram.setter
    def available_ram(self, value):
        self.__available_ram = value

    @property
    def available_disk(self):
        return self.__available_disk

    @available_disk.setter
    def available_disk(self, value):
        self.__available_disk = value

    @property
    def number_master_nodes(self):
        return self.__number_master_nodes

    @number_master_nodes.setter
    def number_master_nodes(self, value):
        self.__number_master_nodes = value

    @property
    def number_worker_nodes(self):
        return self.__number_worker_nodes

    @number_worker_nodes.setter
    def number_worker_nodes(self, value):
        self.__number_worker_nodes = value

    @property
    def storage_type(self):
        return self.__storage_type

    @storage_type.setter
    def storage_type(self, value):
        self.__storage_type = value

    @property
    def storage_name(self):
        return self.__storage_name

    @storage_name.setter
    def storage_name(self, value):
        self.__storage_name = value

    @property
    def storage_host(self):
        return self.__storage_host

    @storage_host.setter
    def storage_host(self, value):
        self.__storage_host = value

    @property
    def export_path(self):
        return self.__export_path

    @export_path.setter
    def export_path(self, value):
        self.__export_path = value

    @property
    def subdomain_name(self):
        return self.__subdomain_name

    @subdomain_name.setter
    def subdomain_name(self, value):
        self.__subdomain_name = value

    @property
    def sample_apps(self):
        return self.__sample_apps

    @sample_apps.setter
    def sample_apps(self, value):
        self.__sample_apps = value
