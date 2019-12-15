from django.urls import path, re_path

from .views import PlaceView


urlpatterns = [
    path('<int:pid>/', PlaceView.as_view(), name='place'),
]