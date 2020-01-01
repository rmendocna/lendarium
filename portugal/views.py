from itertools import chain

from django.conf import settings
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView

from mptt.utils import drilldown_tree_for_node

from legends.views import PAGE_ITEMS

from .models import Region


class PlaceView(DetailView):

    model = Region

    pk_url_kwarg = 'pid'
    _page = 1

    def get(self, request, *args, **kwargs):
        if 'page' in request.GET:
            self._page = int(request.GET['page'])
        return super(PlaceView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PlaceView, self).get_context_data(**kwargs)
        place = context['object']
        descendants = context['object'].get_descendants(include_self=True)
        collections = []
        collections += [place.collections.all() for place in descendants]
        collections = sorted(set(chain(*collections)), key=lambda x: x.pk)
        paginator = Paginator(collections, PAGE_ITEMS)
        page = paginator.get_page(self._page)

        context.update(dict(
            map_token=settings.MAPBOX_TOKEN,
            object_list=page.object_list,
            page_obj=page,
            is_region=True,
            drilldown=drilldown_tree_for_node(place),
        ))
        return context
