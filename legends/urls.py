from django.urls import path
# from django.views.decorators.cache import cache_page

from .views import (CategoryPlacesListApi, NarrativeListView, NarrativeView, SearchView, NarrativeListTag,
                    PlacesListApi, SearchAllView)


urlpatterns = [
    path('tag/<int:tid>/', NarrativeListTag.as_view(), name='tag-detail'),
    path('search/', SearchAllView.as_view(), name='search'),
    path('api/places/', PlacesListApi.as_view(), name='api-places'),
    path('api/<slug:category>/places/', CategoryPlacesListApi.as_view(), name='api-category-places'),
    path('<slug:category>/search/', SearchView.as_view(), name='search-category'),
    path('<slug:category>/', NarrativeListView.as_view(), name='category-detail'),
    path('<slug:slug>/', NarrativeView.as_view(), name='narrative-detail'),
    path('<slug:category>/<slug:slug>/', NarrativeView.as_view(), name='narrative-detail'),
]