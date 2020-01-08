from django.urls import path

from .views import CategoryPlacesListApi, NarrativeListView, NarrativeView, SearchView, NarrativeListTag


urlpatterns = [
    path('tag/<int:tid>/', NarrativeListTag, name='tag-detail'),
    path('api/<slug:category>/places/', CategoryPlacesListApi.as_view(), name='api-category-places'),
    path('<slug:category>/search/', SearchView.as_view(), name='search-category'),
    path('<slug:category>/', NarrativeListView.as_view(), name='category-detail'),
    path('<slug:slug>/', NarrativeView.as_view(), name='narrative-detail'),
    path('<slug:category>/<slug:slug>/', NarrativeView.as_view(), name='narrative-detail'),
]