from django import template
from django.utils.safestring import mark_safe
import datetime

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
def displayFilter(filter_column, configTableClass, filter_conditions):
    try:
        selectDom = '<select name="%s">' % filter_column
        columnObj = configTableClass.model._meta.get_field( filter_column )
        for choice in columnObj.get_choices():
            selected = ''
            if str(choice[0]) == filter_conditions.get(filter_column):
                selected = 'selected'
            selectDom += '<option value="%s" %s>%s</option>' % (choice[0], selected, choice[1])
    except AttributeError as e:
        selectDom = '<select name="%s__gte">' % filter_column
        todayObj = datetime.datetime.now()
        dateChoicesList = [
            ['','------'],
            [todayObj,'Today'],
            [todayObj-datetime.timedelta(7), 'A week'],
            [todayObj.replace(day=1), 'The month'],
            [todayObj.replace(month=1, day=1), 'The year'],
        ]
        for choice in dateChoicesList:
            selected = ''
            choice[0] = '' if not choice[0] else '%s-%s-%s'%(choice[0].year, choice[0].month, choice[0].day)
            if str(choice[0]) == filter_conditions.get('%s__gte'%filter_column):
                selected = 'selected'
            selectDom += '<option value="%s" %s>%s</option>'%(choice[0], selected, choice[1])

    selectDom += '</select>'
    return mark_safe(selectDom)

