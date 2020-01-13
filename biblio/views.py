from django.conf import settings
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView

from legends.views import PAGE_ITEMS

from .models import Volume


class BiblioList(ListView):

    model = Volume
    paginate_by = PAGE_ITEMS


class BiblioView(DetailView):

    model = Volume

    pk_url_kwarg = 'vid'
    _page = 1

    def get(self, request, *args, **kwargs):
        if 'page' in request.GET:
            self._page = int(request.GET['page'])
        return super(BiblioView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BiblioView, self).get_context_data(**kwargs)
        paginator = Paginator(self.object.citations.all(), PAGE_ITEMS)
        page = paginator.get_page(self._page)

        context.update(dict(
            object_list=page.object_list,
            is_biblio=True,
            map_token=settings.MAPBOX_TOKEN,
            page_obj=page,
        ))
        return context
