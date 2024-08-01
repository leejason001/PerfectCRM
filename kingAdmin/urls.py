from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url(r'tableOfOverview-(\w+)-(\w+).html', views.tableOfOverview, name='tableOfOverview'),
    url(r'', views.tablesOfApps,name="tablesOfApps" ),
]
