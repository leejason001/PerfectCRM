from django import conf

def discoverKingAdmin(site):
    for appName in conf.settings.INSTALLED_APPS:
        try:
            mod = __import__( '%s.kingadmin' % appName )
            print(mod)
        except ImportError:
            pass