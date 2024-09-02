from django.shortcuts import render


class BaseKingAdmin(object):
    list_filter = []
    list_display = []
    search_fields = []
    readonly_fields = []
    default_actions = ["delelteSelected"]
    actions = []
    def __init__(self):
        self.actions.extend(self.default_actions)

    def delelteSelected(self, request, appName, tableName, querysets):
        configTableClass = self
        theRowSet = configTableClass.model.objects.filter( id__in=querysets )
        return render( request, 'tableDelete.html', locals())
