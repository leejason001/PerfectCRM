from kingAdmin.BaseKingAdmin import BaseKingAdmin
from kingAdmin import sites
from models import *

class userprofileKingAdmin(BaseKingAdmin):
    list_display = ['name']
sites.site.register(UserProfile, userprofileKingAdmin)

class customerinfoKingAdmin(BaseKingAdmin):
    list_display = ['id','name', 'source', 'consultant', 'contact']
    list_filter  = ['source', 'consultant', 'date']
    search_fields = ['contact', 'consultant__name']
    readonly_fields = ['contact', ]

sites.site.register(CustomerInfo, customerinfoKingAdmin)

sites.site.register(Course)
sites.site.register(ClassList)
