from django import template
from django.utils.safestring import mark_safe
import datetime

register = template.Library()

@register.simple_tag
def displayTheRow(row, list_display):
    response = '<tr>'
    if list_display:
        for item in list_display:
            if row._meta.get_field(item).choices:
                column_data = getattr(row,'get_%s_display'% item)()
            else:
                column_data = getattr(row,item)
            response += '<td>%s</td>'% column_data
    else:
        response += '<td>%s</td>'% row.__str__()
    response += '</tr>'
    return mark_safe(response)

@register.simple_tag
def displayFilter(filter_column, configTableClass, filter_conditions):
    try:
        selectDom = '<select name="%s">' % filter_column
        columnObj = configTableClass.model._meta.get_field( filter_column )
        for choice in columnObj.get_choices():
            selected = ''
            if filter_column in filter_conditions:
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
            if '%s__gte'%filter_column in filter_conditions:
                if str(choice[0]) == filter_conditions.get('%s__gte'%filter_column):
                    selected = 'selected'
            selectDom += '<option value="%s" %s>%s</option>'%(choice[0], selected, choice[1])

    selectDom += '</select>'
    return mark_safe(selectDom)

@register.simple_tag
def get_modelName(configTableClass):
    return configTableClass.model._meta.model_name.upper()

@register.simple_tag
def getPaginators(page_obj):
    MAX_PAGES = 3
    pagerDoms = ''
    pageNumber = 1

    if page_obj.has_previous():
        pagerDoms += '''<li>
          <a href="?page=%s" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>'''%page_obj.previous_page_number()

    while pageNumber <= page_obj.paginator.num_pages:
        if abs(pageNumber - page_obj.number) < MAX_PAGES:
            if pageNumber == page_obj.number:
                thePagerDom = '<li class="active"><span>%s</span></li>'%pageNumber
            else:
                thePagerDom = '<li><a href="?page=%d">%s</a></li>'%(pageNumber,pageNumber)
            pagerDoms += thePagerDom
        pageNumber +=1

    if page_obj.has_next():
        pagerDoms += '''<li>
          <a href="?page=%s" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>'''%page_obj.next_page_number()
    return mark_safe(pagerDoms)

@register.simple_tag
def get_order_index (item, sorted_column, forloopIndex):
    if item in sorted_column:
        if sorted_column[item].startswith('-'):
            new_sorted_index = sorted_column[item].strip('-')
        else:
            new_sorted_index = '-%s'%sorted_column[item]

        return new_sorted_index
    else:
        return forloopIndex

@register.simple_tag
def render_order_triangle (item, sorted_column):
    order_triangle = ''
    if item in sorted_column:
        if sorted_column[item].startswith('-'):
            orderDirection = 'bottom'
        else:
            orderDirection = 'top'
        order_triangle = '<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>'%orderDirection
    return mark_safe(order_triangle)

@register.simple_tag
def render_filtered_paramers(configTableClass):
    paramersString = ''
    for k, v in configTableClass.filter_conditions.items():
        paramersString += '&%s=%s'%(k,v)
    return paramersString




