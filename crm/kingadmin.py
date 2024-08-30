from kingAdmin.BaseKingAdmin import BaseKingAdmin
from kingAdmin import sites
from models import *

class userprofileKingAdmin(BaseKingAdmin):
    list_display = ['name']
sites.site.register(UserProfile, userprofileKingAdmin)

class customerinfoKingAdmin(BaseKingAdmin):
    list_display = ['id','name', 'source', 'consultant', 'status', 'contact']
    list_filter  = ['source', 'consultant', 'date']
    search_fields = ['contact', 'consultant__name']
    readonly_fields = ['contact', ]
    filter_horizontal = ['consult_courses',]
    actions = ['change_status', ]

    def change_status(self, request, querysets):
        querysets.update(status=1)



sites.site.register(CustomerInfo, customerinfoKingAdmin)

sites.site.register(Course)
sites.site.register(ClassList)
sites.site.register(CustomerFollowUp)
