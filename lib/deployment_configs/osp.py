class OSP(object):
    '''
    This class contains all the config information for an OSP
    deployment.
    '''

    @property
    def compute_count(self):
        return self.__compute_count

    @compute_count.setter
    def compute_count(self, value):
        self.__compute_count = value

    @property
    def controller_count(self):
        return self.__controller_count

    @controller_count.setter
    def controller_count(self, value):
        self.__controller_count = value

    @property
    def block_storage_count(self):
        return self.__block_storage_count

    @block_storage_count.setter
    def block_storage_count(self, value):
        self.__block_storage_count = value

    @property
    def object_storage_count(self):
        return self.__object_storage_count

    @object_storage_count.setter
    def object_storage_count(self, value):
        self.__object_storage_count = value

    @property
    def director_address(self):
        return self.__director_address

    @director_address.setter
    def director_address(self, value):
        self.__director_address = value

    @property
    def director_ui_url(self):
        return self.__director_ui_url

    @director_ui_url.setter
    def director_ui_url(self, value):
        self.__director_ui_url = value

    @property
    def director_vm_name(self):
        return self.__director_vm_name

    @director_vm_name.setter
    def director_vm_name(self, value):
        self.__director_vm_name = value

    # TODO:  Need to make over cloud node structure
    @property
    def overcloud_nodes(self):
        return self.__overcloud_nodes

    @overcloud_nodes.setter
    def overcloud_nodes(self, value):
        self.__overcloud_nodes = value

    @property
    def undercloud_address(self):
        return self.__undercloud_address

    @undercloud_address.setter
    def undercloud_address(self, value):
        self.__undercloud_address = value

    @property
    def undercloud_pass(self):
        return self.__undercloud_pass

    @undercloud_pass.setter
    def undercloud_pass(self, value):
        self.__undercloud_pass = value

    @property
    def undercloud_user(self):
        return self.__undercloud_user

    @undercloud_user.setter
    def undercloud_user(self, value):
        self.__undercloud_user = value

    # TODO:  Need to make network structure.
    @property
    def network(self):
        return self.__network

    @network.setter
    def network(self, value):
        self.__network = value
