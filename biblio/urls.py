from django.urls import path

from .views import BiblioView, BiblioList


urlpatterns = [
    path('', BiblioList.as_view(), name='biblio'),
    path('<int:vid>/', BiblioView.as_view(), name='volume'),
]