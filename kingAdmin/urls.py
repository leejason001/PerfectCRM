from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url(r'', views.tablesOfApps,name="tablesOfApps" ),
]
