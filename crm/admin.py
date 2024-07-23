# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models

# Register your models here.
admin.site.register(models.CustomerInfo)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.ClassList)
admin.site.register(models.Course)
admin.site.register(models.Role)
admin.site.register(models.Menus)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
admin.site.register(models.Student)
admin.site.register(models.UserProfile)
