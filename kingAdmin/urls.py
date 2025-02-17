from django.conf.urls import url
from django.contrib import admin

import views

urlpatterns = [
    url( r'^/(\w+)/(\w+)/tableOfOverview.html$', views.tableOfOverview, name='tableOfOverview' ),
    url(r'^/(\w+)/(\w+)/(\d+)/change$', views.tableChange, name='tableChange'),
    url(r'^/(\w+)/(\w+)/(\d+)/delete$', views.tableDelete, name='tableDelete'),
    url(r'^/(\w+)/(\w+)/add$', views.tableAdd, name='tableAdd'),
    url(r'', views.tablesOfApps,name="tablesOfApps" ),
]
