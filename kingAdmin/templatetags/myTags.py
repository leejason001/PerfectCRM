from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def displayTheRow(row, list_display):
    response = '<tr>'
    for item in list_display:
        domEle = '<td>%s</td>'%getattr(row,item)
        response += domEle
    response += '</tr>'
    return mark_safe(response)
