from django import template
from django.utils.safestring import mark_safe
import datetime

register = template.Library()


@register.simple_tag
def displayTheRow(row, list_display):
    response = '<tr><td><input type="checkbox" tagForSelect value=%s></td>'%row.id
    if list_display:
        for index, item in enumerate(list_display):
            if row._meta.get_field(item).choices:
                column_data = getattr(row,'get_%s_display'% item)()
            else:
                column_data = getattr(row,item)
            if 0 == index:
                response += "<td><a href='%s/change'>%s</a></td>" % (row.id, column_data)
            else:
                response += '<td>%s</td>'% column_data
    else:
        response += "<td><a href='%s/change'>%s</a></td>"% (row.id, row.__str__())
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
def render_filtered_paramers(configTableClass):
    if configTableClass.filter_conditions:
        paramersString = ''
        for k, v in configTableClass.filter_conditions.items():
            paramersString += '&%s=%s'%(k,v)
        return paramersString
    else:
        return ''

@register.simple_tag
def getPaginators(page_obj, configTableClass, sorted_column):
    MAX_PAGES = 3
    pagerDoms = ''
    pageNumber = 1
    filtered_paramers = render_filtered_paramers( configTableClass )

    order_paramers = ''
    if sorted_column:
        order_paramers = '&o='
        order_paramers += list(sorted_column.values())[0]

    if page_obj.has_previous():
        pagerDoms += '''<li>
          <a href="?page=%s%s%s" aria-label="Previous">
            <span aria-hidden="true">&laquo;</span>
          </a>
        </li>'''%(page_obj.previous_page_number(), filtered_paramers, order_paramers)

    while pageNumber <= page_obj.paginator.num_pages:
        if abs(pageNumber - page_obj.number) < MAX_PAGES:
            if pageNumber == page_obj.number:
                thePagerDom = '<li class="active"><span>%s</span></li>'%pageNumber
            else:
                thePagerDom = '<li><a href="?page=%d%s%s">%s</a></li>'%(pageNumber,filtered_paramers,order_paramers, pageNumber)
            pagerDoms += thePagerDom
        pageNumber +=1

    if page_obj.has_next():
        pagerDoms += '''<li>
          <a href="?page=%s%s%s" aria-label="Next">
            <span aria-hidden="true">&raquo;</span>
          </a>
        </li>'''%(page_obj.next_page_number(), filtered_paramers, order_paramers)
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
def get_order_paramers(sorted_column):

        return list(sorted_column.values())[0] if sorted_column else ''

@register.simple_tag
def get_formObj_field_value(form_obj, field):
    return getattr(form_obj.instance, field)

@register.simple_tag
def get_remainder(fieldName, form_obj, theModel):
    theWholeSet  = set(theModel._meta.get_field(fieldName).related_model.objects.all())
    try:
        theSelectSet = set(getattr(form_obj.instance, fieldName).all())
        return theWholeSet - theSelectSet
    except:
        return theWholeSet

@register.simple_tag
def get_selected(fieldName, form_obj):
    try:
        theRowObj = form_obj.instance
        return getattr(theRowObj, fieldName).all()
    except:
        return []

@register.simple_tag
def display_all_related_rows(theRow):
    responseStr = '<ul><li><a href="/kingAdmin/%s/%s/%s/change">%s</a>'%(theRow._meta.app_label,
                                                 theRow._meta.model_name, theRow.id, theRow)
    responseStr += '</li>'
    for reverse_fk_obj in theRow._meta.related_objects:
        related_table_name = reverse_fk_obj.name
        related_lookup_key = "%s_set"%related_table_name
        responseStr += '<li>%s'%related_table_name
        responseStr += '<ul>'
        if reverse_fk_obj.get_internal_type() == "ManyToManyField":
            for subRow in getattr( theRow, related_lookup_key ).all():
                responseStr += '<li><a href="/kingAdmin/%s/%s/%s/change">%s</a></li>' % (subRow._meta.app_label,
                                                          subRow._meta.model_name, subRow.id, subRow)
        else:
            print(related_lookup_key)
            print(getattr( theRow, related_lookup_key ).all())
            for subRow in getattr( theRow, related_lookup_key ).all():
                responseStr += display_all_related_rows( subRow )

        responseStr += '</ul></li>'

    responseStr += '</ul>'
    return responseStr








