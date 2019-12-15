from django.urls import path

from .views import CategoryPlacesListApi, NarrativeListView, NarrativeView, SearchView


urlpatterns = [
    path('<slug:slug>/search/', SearchView.as_view(), name='search-category'),
    path('<slug:slug>/', NarrativeListView.as_view(), name='category-detail'),
    path('api/<slug:slug>/places/', CategoryPlacesListApi.as_view(), name='api-category-places'),
    path('<slug:slug>/', NarrativeView.as_view(), name='narrative-detail'),
    path('<slug:category>/<slug:slug>/', NarrativeView.as_view(), name='narrative-detail'),
]