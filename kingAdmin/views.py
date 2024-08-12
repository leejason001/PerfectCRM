# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import  login_required
from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator

from kingAdmin import sites
from kingAdmin.app_setup import discoverKingAdmin


discoverKingAdmin(sites.site)
# Create your views here.
@login_required
def tablesOfApps(request):
    for appName, tables in sites.site.enabled_admin.items():
        print(appName)
    return render(request, 'tablesOfApps.html', {'apps': sites.site.enabled_admin})

def getFilterConditions(request):
    filter_conditions = {}
    for k, v in request.GET.items():
        if 'page' == k:
            continue
        if v:
            filter_conditions[k] = v
    return filter_conditions
@login_required
def tableOfOverview(request, appName, tableName):
    configTableClass = sites.site.enabled_admin[appName][tableName]
    rows = configTableClass.model.objects.all()
    filter_conditions = getFilterConditions(request)
    rowsQuerySet = rows.filter(**filter_conditions)

    paginator = Paginator(rowsQuerySet, 1)
    rowsQuerySet = paginator.page(request.GET.get('page',1))

    return render(request, 'tableOfOverview.html',{'configTableClass':configTableClass, 'filter_conditions':filter_conditions,
                                                   'rows':rowsQuerySet})





