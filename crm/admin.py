# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'source', 'consultant', 'contact_type','status', 'date']
    list_filter = ['source', 'consultant', 'status', 'date']
    search_fields = ['source', 'consultant__name']
    filter_horizontal = ['consult_courses', ]


# Register your models here.
admin.site.register(models.CustomerInfo, CustomerAdmin)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.ClassList)
admin.site.register(models.Course)
admin.site.register(models.Role)
admin.site.register(models.Menus)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
admin.site.register(models.Student)
admin.site.register(models.UserProfile)
admin.site.register(models.Branch)
