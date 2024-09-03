from django.shortcuts import render, redirect
import json



class BaseKingAdmin(object):
    list_filter = []
    list_display = []
    search_fields = []
    readonly_fields = []
    default_actions = ["delelteSelected"]
    actions = []
    def __init__(self):
        self.actions.extend(self.default_actions)

    def delelteSelected(self, request, appName, tableName, querysets, rowsQuerySet, sorted_column):
        configTableClass = self
        theRowSet = configTableClass.model.objects.filter( id__in=querysets )
        if "POST" == request.method:
            if "yes" == request.POST.get("delete_confirm"):
                theRowSet.delete()
                return redirect("/kingAdmin/%s/%s"%(appName, tableName))
        return render( request, 'tableDelete.html', locals())
