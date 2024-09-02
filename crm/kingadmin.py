from django.shortcuts import render

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

    def change_status(self, request, appName, tableName, querysets, rowsQuerySet, sorted_column):
        querysets.update(status=1)
        return render( request, 'tableOfOverview.html',
                       {'configTableClass': self, 'filter_conditions': self.filter_conditions,
                        'rows': rowsQuerySet, 'sorted_column': sorted_column} )



sites.site.register(CustomerInfo, customerinfoKingAdmin)

sites.site.register(Course)
sites.site.register(ClassList)
sites.site.register(CustomerFollowUp)
