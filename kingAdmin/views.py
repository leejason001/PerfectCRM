# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import  login_required
from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import ModelForm

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
        if k in ('page', 'o', '_q'):
            continue
        if v:
            filter_conditions[k] = v
    return filter_conditions

def doSearch(request, configTableClass, rowsQuerySet):
    configTableClass.searchContent = request.GET.get('_q','')
    searchContents = configTableClass.searchContent.split(',')
    if searchContents:
        q1 = Q()
        q1.connector = 'OR'
        for searchItem in configTableClass.search_fields:
            for content in searchContents:
                content = content.strip(',')
                q1.children.append(('%s__contains'%searchItem, content))
        return rowsQuerySet.filter(q1)
    else:
        return rowsQuerySet

@login_required
def tableOfOverview(request, appName, tableName):

    configTableClass = sites.site.enabled_admin[appName][tableName]
    rows = configTableClass.model.objects.all()
    configTableClass.filter_conditions = getFilterConditions(request)
    rowsQuerySet = rows.filter(**configTableClass.filter_conditions).order_by("-id")

    rowsQuerySet = doSearch(request, configTableClass, rowsQuerySet)


    orderIndexAndDirection = request.GET.get('o')
    sorted_column = {}
    if orderIndexAndDirection:
        orderColumn = configTableClass.list_display[abs( int( orderIndexAndDirection ) )]
        sorted_column[orderColumn] = orderIndexAndDirection
        if orderIndexAndDirection.startswith( '-' ):
            rowsQuerySet = rowsQuerySet.order_by( '-%s' % orderColumn )
        else:
            rowsQuerySet = rowsQuerySet.order_by( orderColumn )



    paginator = Paginator(rowsQuerySet, 2)
    rowsQuerySet = paginator.page(request.GET.get('page',1))

    return render(request, 'tableOfOverview.html',{'configTableClass':configTableClass, 'filter_conditions':configTableClass.filter_conditions,
                                                   'rows':rowsQuerySet, 'sorted_column':sorted_column})

def create_dynamic_model_form(configTableClass, form_add=False):

    class Meta:
        model = configTableClass.model
        fields = "__all__"

        if not form_add:
            exclude = configTableClass.readonly_fields
            configTableClass.need_readonly = True
        else:
            configTableClass.need_readonly = False

    def __new__(cls, *args, **kwargs):

        for field_name in cls.base_fields:

            field_obj = cls.base_fields[field_name]

            field_obj.widget.attrs.update({"class":"form-control"})
        return ModelForm.__new__(cls)

    theModelForm = type("DynamicModelForm".encode('ascii'), (ModelForm, ), {'Meta':Meta, '__new__':__new__})

    return theModelForm

@login_required
def tableChange(request, appName, modelName, rowId):
    configTableClass = sites.site.enabled_admin[appName][modelName]
    theModelForm = create_dynamic_model_form(configTableClass)
    rowData = configTableClass.model.objects.filter(id=rowId)[0]
    if 'GET' == request.method:
        form_obj = theModelForm(instance=rowData)
    elif 'POST' == request.method:
        form_obj = theModelForm(instance=rowData, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/kingAdmin/%s/%s"%(appName, modelName))
    return render( request, 'tableChange.html', locals())

@login_required
def tableAdd(request, appName, modelName):
    configTableClass = sites.site.enabled_admin[appName][modelName]

    theModelForm     = create_dynamic_model_form(configTableClass, True)

    if 'GET'== request.method:
        form_obj = theModelForm()
    elif 'POST' == request.method:
        form_obj = theModelForm(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/kingAdmin/%s/%s"%(appName, modelName))

    return render( request, 'tableAdd.html', locals())





