from django import template
from django.template.loader import get_template

register = template.Library()


def page_index(page_obj, style=""):
    idx = []
    if page_obj and page_obj.has_other_pages():
        if page_obj.has_previous():
            prv = page_obj.previous_page_number()
            idx = [i for i in range(1, min(3, prv))]
            if prv > 3:
                idx += ['..']
            idx += [prv]
        idx += [page_obj.number]
        if page_obj.has_next():
            nxt = page_obj.next_page_number()
            end = page_obj.paginator.num_pages + 1
            idx += [i for i in range(nxt, min(nxt+1, end))]
            if end > nxt + 1:
                if end - 2 > nxt + 1:
                    idx += ['..']
                idx += [i for i in range(max(nxt+1, end-2), end)]
    return {'idx': idx, 'pg': page_obj, 'style': style }


t = get_template('legends/inc_page_index.html')
register.inclusion_tag(t)(page_index)
