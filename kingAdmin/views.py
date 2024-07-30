# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def tablesOfApps(request):
    return render(request, 'tablesOfApps.html')

