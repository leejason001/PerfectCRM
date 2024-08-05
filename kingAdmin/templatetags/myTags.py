from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def displayTheRow(row, list_display):
    response = '<tr>'
    for item in list_display:
        if row._meta.get_field(item).choices:
            column_data = getattr(row,'get_%s_display'% item)()
        else:
            column_data = getattr(row,item)

        response += '<td>%s</td>'% column_data
    response += '</tr>'
    return mark_safe(response)

@register.simple_tag
def displayFilter(filter_column, configTableClass):
    selectDom = '<select name=%s>' % filter_column
    columnObj = configTableClass.model._meta.get_field(filter_column)
    for choice in columnObj.get_choices():
        selectDom += '<option value=%s>%s</option>'%choice
    selectDom += '</select>'
    return mark_safe(selectDom)

