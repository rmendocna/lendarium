from django import template

register = template.Library()


@register.inclusion_tag('legends/inc_page_index.html', takes_context=True)
def page_index(context, page_obj, style=""):
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
    if context['request'].method == 'POST':
        query = context['request'].POST.get('query', None)
    else:
        query = context['request'].GET.get('query', None)

    return {'idx': idx, 'pg': page_obj, 'style': style, 'query': query}
