from kingAdmin.BaseKingAdmin import BaseKingAdmin

class adminSite(object):
    def __init__(self):
        self.enabled_admin = {}

    def register(self, modelClass, configModelClass=None):
        appName        = modelClass._meta.app_label
        modelClassName = modelClass._meta.model_name
        if not configModelClass:
            configModelClass = BaseKingAdmin()
        else:
            configModelClass = configModelClass()
        if appName not in self.enabled_admin:
            self.enabled_admin[appName] = {}

        self.enabled_admin[appName][modelClassName] = configModelClass


site = adminSite()