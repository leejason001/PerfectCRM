# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import  login_required
from django.db.utils import IntegrityError


from crm import models
import myForms

# Create your views here.
@login_required
def dashboard(request):
    return render(request, 'crm/dashboard.html')

@login_required
def stu_enrollment(request):
    customerInfoes = models.CustomerInfo.objects.all()
    theClasses     = models.ClassList.objects.all()
    if "POST" == request.method:
        customer_id=request.POST.get('customer')
        class_grade_id = request.POST.get( "class_grade" )
        try:
            theEnrollment = models.StudentEnrollment.objects.create(
                customer_id=customer_id,
                class_grade_id=class_grade_id,
                consultant_id=request.user.userprofile.id
            )

        except IntegrityError as e:
            theEnrollment = models.StudentEnrollment.objects.get(customer_id=customer_id, class_grade_id=class_grade_id)

        theLink = "http://127.0.0.1:8000/crm/enrollment/%s/" % theEnrollment.id

    return render(request, 'crm/stu_enrollment.html',locals())

def enrollment(request, enrollment_id):
    theEnrollment = models.StudentEnrollment.objects.get(id=enrollment_id)

    if "POST" == request.method:
        customer_form = myForms.CustomerForm( instance=theEnrollment.customer, data=request.POST )#修改数据必须这么写
        if customer_form.is_valid():
                customer_form.save()#theEnrollment.customer.update(**obj.cleaned_data)
                return HttpResponse("You enroll success!")
    else:
        customer_form = myForms.CustomerForm( instance=theEnrollment.customer )

    return render(request, 'crm/enrollment.html', locals())
