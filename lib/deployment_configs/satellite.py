class Satellite(object):
    '''
    This class contains all the satellite config information for a
    deployment.
    '''

    @property
    def deploy_org(self):
        return self.__deploy_org

    @deploy_org.setter
    def deploy_org(self, value):
        self.__deploy_org = value

    @property
    def disconnected_manifest(self):
        return self.__disconnected_manifest

    @disconnected_manifest.setter
    def disconnected_manifest(self, value):
        self.__disconnected_manifest = value

    @property
    def disconnected_url(self):
        return self.__disconnected_url

    @disconnected_url.setter
    def disconnected_url(self, value):
        self.__disconnected_url = value

    @property
    def enable_access_insights(self):
        return self.__enable_access_insights

    @enable_access_insights.setter
    def enable_access_insights(self, value):
        self.__enable_access_insights = value

    @property
    def env_path(self):
        return self.__env_path

    @env_path.setter
    def env_path(self, value):
        self.__env_path = value

    @property
    def use_default_org_view(self):
        return self.__use_default_org_view

    @use_default_org_view.setter
    def use_default_org_view(self, value):
        self.__use_default_org_view = value

    @property
    def disconnected_mode(self):
        return self.__disconnected_mode

    @disconnected_mode.setter
    def disconnected_mode(self, value):
        self.__disconnected_mode = value

    @property
    def sat_desc(self):
        return self.__sat_desc

    @sat_desc.setter
    def sat_desc(self, value):
        self.__sat_desc = value

    @property
    def sat_name(self):
        return self.__sat_name

    @sat_name.setter
    def sat_name(self, value):
        self.__sat_name = value

    @property
    def update_lifecycle_immediately(self):
        return self.__update_lifecycle_immediately

    @update_lifecycle_immediately.setter
    def update_lifecycle_immediately(self, value):
        self.__update_lifecycle_immediately = value

    @property
    def create_new_env(self):
        return self.__create_new_env

    @create_new_env.setter
    def create_new_env(self, value):
        self.__create_new_env = value

    @property
    def rhsm_satellite(self):
        return self.__rhsm_satellite

    @rhsm_satellite.setter
    def rhsm_satellite(self, value):
        self.__rhsm_satellite = value

    @property
    def rhsm_subs(self):
        return self.__rhsm_subs

    @rhsm_subs.setter
    def rhsm_subs(self, value):
        self.__rhsm_subs = value

    @property
    def new_env(self):
        return self.__new_env

    @new_env.setter
    def new_env(self, value):
        self.__new_env = value
