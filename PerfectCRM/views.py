# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def acc_login(request):
    error_msg = ''
    if request.method == "POST":
        username = request.POST.get( 'username' )
        password = request.POST.get( 'password' )

        user = authenticate( username=username, password=password )
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/crm/'))
        else:
            error_msg = "wwwwwrong username or password!"
    return render(request, 'crm/login.html', {'error_msg':error_msg})

def acc_logout(request):
    logout(request)
    return redirect('/login/')
