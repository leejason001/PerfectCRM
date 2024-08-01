# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import  login_required
from django.shortcuts import render, redirect, HttpResponse

from kingAdmin import sites
from kingAdmin.app_setup import discoverKingAdmin


discoverKingAdmin(sites.site)
# Create your views here.
@login_required
def tablesOfApps(request):
    for appName, tables in sites.site.enabled_admin.items():
        print(appName)
    return render(request, 'tablesOfApps.html', {'apps': sites.site.enabled_admin})

