from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.utils.translation import get_language
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from tagging.models import Tag
from tagging.utils import calculate_cloud

from .models import Narrative, Category

PAGE_ITEMS = 30


def old_category_redirect(request, id, page=1):
    cat = Category.objects.get(id__exact=int(id))
    return redirect('category-detail', slug=cat.slug)


class LangMixin(object):

    _lang = None

    def get_lang_field(self, field_name):
        if not self._lang:
            self._lang = get_language()
        return '{}_{}'.format(field_name, self._lang)


class ListMixin(LangMixin):

    paginate_by = PAGE_ITEMS

    def _get_queryset(self):
        return super(ListMixin, self).get_queryset().select_related('collection_place'
                                                                        ).prefetch_related('many_places')


class CategoryMixin(ListMixin):

    _category = None
    model = Narrative

    @property
    def category(self):
        if not self._category:
            slug_field = self.get_lang_field('slug')
            if 'category' in self.kwargs:
                self._category = Category.objects.get(**{slug_field: self.kwargs['category']})
        return self._category

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
        sample = context['object_list']
        if context['category'] and not sample.count():
            descendant_ids = context['category'].get_descendants().values_list('pk', flat=True)
            sample = Narrative.objects.filter(narrativecategory_related__legendcategory_id__in=descendant_ids)
        tags = []
        c = 10
        while len(tags) < 30 and c > 1:
            c -= 1
            tags = Tag.objects.usage_for_queryset(sample, min_count=c)

        context.update(dict(
            categories=Category.objects.filter(parent__isnull=True),
            map_token=settings.MAPBOX_TOKEN,
            cloud=calculate_cloud(tags, steps=9),
        ))
        return context


class NarrativeListTag(ListMixin, DetailView):

    template_name = 'legends/tag.html'
    model = Tag
    pk_url_kwarg = 'tid'
    _page = 1

    def get(self, request, *args, **kwargs):
        if 'page' in request.GET:
            self._page = int(request.GET['page'])
        return super(NarrativeListTag, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NarrativeListTag, self).get_context_data(**kwargs)
        if context['object']:
            paginator = Paginator(context['object'].items.all(), PAGE_ITEMS)
            page = paginator.get_page(self._page)
            context.update(dict(
                object_list=[taggeditem.object for taggeditem in page.object_list],
                map_token=settings.MAPBOX_TOKEN,
                page_obj=page,
            ))
        return context


class SearchView(NarrativeListView):

    template_name = 'legends/search.html'

    def get_queryset(self):
        query = SearchQuery(self.request.GET['query'])
        vector = SearchVector('title', 'transcription', self.get_lang_field('keywords'),
                              self.get_lang_field('common_title'))
        qs = self._get_queryset()
        categories = self.category.get_descendants(include_self=True)
        results = qs.filter(narrativecategory_related__legendcategory_id__in=categories.values_list('id', flat=True)
                            ).annotate(rank=SearchRank(vector, query)).filter(rank__gt=0.0).order_by('-rank')
        return results

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context.update(dict(
            is_search=True,
            map_token=settings.MAPBOX_TOKEN,
        ))
        return context


class SearchAllView(LangMixin, ListView):

    model = Narrative
    template_name = 'legends/search.html'
    paginate_by = PAGE_ITEMS

    def get_queryset(self):
        query = SearchQuery(self.request.GET['query'])
        vector = SearchVector('title',  'transcription', self.get_lang_field('keywords'),
                              self.get_lang_field('common_title'))
        qs = super(SearchAllView, self).get_queryset().defer('rating', 'notes', 'other')
        results = qs.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0.0).order_by('-rank')
        return results

    def get_context_data(self, **kwargs):
        context = super(SearchAllView, self).get_context_data(**kwargs)
        context.update(dict(
            is_search=True,
            map_token=settings.MAPBOX_TOKEN,
        ))
        return context


class NarrativeView(LangMixin, DetailView):

    template_name = 'legends/narrative.html'
    model = Narrative

    def get_slug_field(self):
        lang = get_language()
        return 'slug_{}'.format(lang)

    def get_context_data(self, **kwargs):
        context = super(NarrativeView, self).get_context_data(**kwargs)
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
