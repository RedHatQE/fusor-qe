class CFME(object):
    '''
    This class contains all the config information for a CFME
    deployment.
    '''

    @property
    def cfme_address(self):
        return self.__cfme_address

    @cfme_address.setter
    def cfme_address(self, value):
        self.__cfme_address = value

    @property
    def cfme_admin_password(self):
        return self.__cfme_admin_password

    @cfme_admin_password.setter
    def cfme_admin_password(self, value):
        self.__cfme_admin_password = value

    @property
    def cfme_install_loc(self):
        return self.__cfme_install_loc

    @cfme_install_loc.setter
    def cfme_install_loc(self, value):
        self.__cfme_install_loc = value

    @property
    def cfme_root_password(self):
        return self.__cfme_root_password

    @cfme_root_password.setter
    def cfme_root_password(self, value):
        self.__cfme_root_password = value

    @property
    def cfme_db_password(self):
        return self.__cfme_db_password

    @cfme_db_password.setter
    def cfme_db_password(self, value):
        self.__cfme_db_password = value

