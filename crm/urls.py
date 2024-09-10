from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url(r'^$', views.dashboard,name="sales_dashboard" ),
    url(r'^stu_enrollment/$', views.stu_enrollment, name="stu_enrollment"),
    url(r'^enrollment/(\d+)/$', views.enrollment, name="enrollment"),
]
