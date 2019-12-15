# import json

from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import get_language
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Narrative, Category
from portugal.models import Region


def old_category_redirect(request, id, page=1):
    cat = Category.objects.get(id__exact=int(id))
    return redirect('category-detail', slug=cat.slug)


PAGE_ITEMS = 30


class LangMixin:

    def get_lang_field(self, field_name):
        if not self._lang:
            self._lang = get_language()
        return '{}_{}'.format(field_name, self._lang)


class CategoryMixin(LangMixin):

    _category = None
    _lang = None
    model = Narrative
    paginate_by = PAGE_ITEMS

    @property
    def category(self):
        if not self._category:
            slug_field = self.get_lang_field('slug')
            self._category = Category.objects.get(**{slug_field: self.kwargs['slug']})
        return self._category

    def _get_queryset(self):
        return super(CategoryMixin, self).get_queryset().select_related('collection_place'
                                                                        ).prefetch_related('many_places')

    def get_queryset(self):
        qs = self._get_queryset()
        return qs.filter(narrativecategory_related__legendcategory_id=self.category.pk)

    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context.update(dict(
            category=self.category
        ))
        return context


class NarrativeListView(CategoryMixin, ListView):

    template_name = 'legends/category.html'

    def get_context_data(self, **kwargs):
        context = super(NarrativeListView, self).get_context_data(**kwargs)
        context.update(dict(
            categories=Category.objects.filter(parent__isnull=True),
            map_token=settings.MAPBOX_TOKEN,
        ))
        return context


class CategoryPlacesListApi(CategoryMixin, ListView):

    response_class = HttpResponse

    def get_context_data(self, **kwargs):
        context = super(CategoryPlacesListApi, self).get_context_data(**kwargs)
        # places = [ol.collection_place for ol in context['object_list']]
        narratives = context['object_list']
        collections = serialize('geojson', narratives, geometry_field='collection_place__mpoly',
                                use_natural_foreign_keys=True, use_natural_primary_keys=True,
                                fields=('collection_place__parent__name', 'collection_place__name'))
        return collections

    def render_to_response(self, context, **response_kwargs):
        kwargs = response_kwargs or {}
        kwargs.update(dict(content_type='application/json'))
        return self.response_class(context, **kwargs)


class SearchView(NarrativeListView):

    template_name = 'legends/search.html'

    def get_queryset(self):
        query = SearchQuery(self.request.GET['query'])
        vector = SearchVector('title', self.get_lang_field('keywords'), self.get_lang_field('common_title'))
        qs = super(SearchView, self)._get_queryset()
        categories = self.category.get_descendants(include_self=True)
        return qs.filter(narrativecategory_related__legendcategory_id__in=categories.values_list('id', flat=True)
                         ).annotate(rank=SearchRank(vector, query))


class NarrativeView(LangMixin, DetailView):

    template_name = 'legends/narrative.html'
    model = Narrative

    def get_slug_field(self):
        lang = get_language()
        return 'slug_{}'.format(lang)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category', '')
        if not category_slug:
            category = context['object'].categories.first()
        else:
            slug_field = self.get_slug_field()
            params = {slug_field: category_slug}
            category = Category.objects.get(**params)
        context['category'] = category
        context['categories'] = Category.objects.filter(parent__isnull=True)
        return context


def category_by_id(request, cid):

    cat = Category.objects.get(pk=cid)
    return redirect('category-detail', slug=cat.slug)


def legend_by_id(request, nid, cid=None):

    narr = Narrative.objects.get(pk=nid)
    if not cid:
        cat = narr.categories.first()
    else:
        cat = Category.objects.get(pk=cid)
    return redirect('narrative-detail', category=cat.slug, slug=narr.slug)


def search(request):
    if 'REFERER' not in request.META:
        return HttpResponseBadRequest
    keys = ('title', 'keywords')
    if request.method == 'POST':
        keys += ('transcription',)
        query = SearchQuery(request.POST['query'])
    else:
        query = SearchQuery(request.GET['query'])
    vector = SearchVector(keys)
    legends = Narrative.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')
    paginator = Paginator(legends, PAGE_ITEMS)
    object_list = paginator.object_list
    return render(request, 'lengends/search.html', {'paginator': paginator, 'object_list': object_list})


def place(request, initial, pid):
    kwargs = {'extra_context': {}}
    if initial in ['p', 'f']:  # its a parish
        place = Region.objects.get(id=pid)
        queryset = Narrative.objects.filter(is_public=True, collection_place__parish=place)
        kwargs['extra_context']['place']
    # else:  # it's a council
    #     place = Concelho.objects.get(id=int(pid))
    #     queryset = Narrative.objects.filter(is_public=True, collection_place__concelho=place)
    mpolys = [GPolygon(kwargs['extra_context']['place'].mpoly.tuple[0][0], stroke_color="#000000", stroke_weight=1,
                       fill_color="#666666")]
    kwargs['extra_context']['map'] = GoogleMap(polygons=mpolys)
    kwargs['template_object_name'] = 'narrative'
    tags = list(Tag.objects.usage_for_queryset(queryset, counts=True))
    kwargs['extra_context']['cloud'] = calculate_cloud(tags, steps=9)
    return render(request, queryset, kwargs)

