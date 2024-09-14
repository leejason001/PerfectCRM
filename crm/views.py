# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.decorators import  login_required
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.timezone import datetime
import os
import json


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
            if True == theEnrollment.contract_agreed:


                return redirect("%s/contract_audit/"%theEnrollment.id)

        theLink = "http://127.0.0.1:8000/crm/enrollment/%s/" % theEnrollment.id

    return render(request, 'crm/stu_enrollment.html',locals())

@login_required
def contract_audit(request, enrollment_id):
    theEnrollment = models.StudentEnrollment.objects.get(id=enrollment_id)
    if "POST" == request.method:
        studentEnrollmentForm = myForms.StudentEnrollmentForm(instance=theEnrollment, data=request.POST)
        if studentEnrollmentForm.is_valid():
            theEnrollment.contract_approved_date = datetime.now()
            theEnrollment.save()
            studentEnrollmentForm.save()
            theStudent = models.Student.objects.get_or_create(customer=theEnrollment.customer)[0]
            theStudent.class_grades.add(theEnrollment.class_grade_id)
            theStudent.save()
            return redirect("/kingAdmin/crm/customerinfo/%s/change"%theEnrollment.customer.id)
    else:
        customerForm = myForms.CustomerForm(instance=theEnrollment.customer)
        studentEnrollmentForm = myForms.StudentEnrollmentForm(instance=theEnrollment)

    return render(request, "crm/contract_audit.html", locals())

def enrollment(request, enrollment_id):
    theEnrollment = models.StudentEnrollment.objects.get(id=enrollment_id)
    if True == theEnrollment.contract_agreed:
        return HttpResponse("正在审核中")
    if "POST" == request.method:
        customer_form = myForms.CustomerForm( instance=theEnrollment.customer, data=request.POST )#修改数据必须这么写
        if customer_form.is_valid():
                customer_form.save()#theEnrollment.customer.update(**obj.cleaned_data)
                theEnrollment.contract_agreed = True
                theEnrollment.contract_signed_date = datetime.now()
                theEnrollment.save()
                return HttpResponse("You enroll success!")
    else:
        customer_form = myForms.CustomerForm( instance=theEnrollment.customer )

    if os.path.isdir(os.path.join( settings.ENROLLMENT_UPLOAD_FILES_DIR, enrollment_id ) ):
        uploadedFiles = os.listdir( os.path.join( settings.ENROLLMENT_UPLOAD_FILES_DIR, enrollment_id ) )


    return render(request, 'crm/enrollment.html', locals())

@csrf_exempt
def enrollment_fileUpLoad(request, enrollment_id):
    fileUpLoadDir = os.path.join(settings.ENROLLMENT_UPLOAD_FILES_DIR, enrollment_id)

    if not os.path.isdir(fileUpLoadDir):
        os.mkdir(fileUpLoadDir)

    if len(os.listdir(fileUpLoadDir)) > 2:
        return HttpResponse(json.dumps({'status':False, 'errMsg':"upload too manany files!"}))
    file_obj = request.FILES.get("file")
    with open(os.path.join(fileUpLoadDir, file_obj.name), 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)


    return HttpResponse(json.dumps({'status':True}))
