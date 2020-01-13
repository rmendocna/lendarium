from django.urls import path

from .views import PlaceView, PlacesListApi


urlpatterns = [
    path('api/places/', PlacesListApi.as_view(), name='api-places'),
    path('<int:pid>/', PlaceView.as_view(), name='place'),
]