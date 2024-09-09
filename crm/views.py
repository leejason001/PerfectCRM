# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import  login_required

from crm import models

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'crm/dashboard.html')

@login_required
def stu_enrollment(request):
    customerInfoes = models.CustomerInfo.objects.all()
    theClasses     = models.ClassList.objects.all()
    if "POST" == request.method:
        theEnrollment = models.StudentEnrollment.objects.create(
            customer_id=request.POST.get('customer'),
            class_grade_id=request.POST.get("class_grade"),
            consultant_id=request.user.userprofile.id
        )
        theLink = "http://127.0.0.1:8000/crm/enrollment/%s/"%theEnrollment.id

    return render(request, 'crm/stu_enrollment.html',locals())
