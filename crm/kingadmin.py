from kingAdmin.BaseKingAdmin import BaseKingAdmin
from kingAdmin import sites
from models import *

class userprofileKingAdmin(BaseKingAdmin):
    list_display = ['name']
sites.site.register(UserProfile, userprofileKingAdmin)

class customerinfoKingAdmin(BaseKingAdmin):
    list_display = ['id','name', 'source', 'consultant']
    list_filter  = ['source', 'consultant', 'date']
sites.site.register(CustomerInfo, customerinfoKingAdmin)

sites.site.register(Course)
sites.site.register(ClassList)
