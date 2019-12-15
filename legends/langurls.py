from django.urls import path

from .views import category_by_id, legend_by_id

urlpatterns = [
    path('<int:cid>/', category_by_id, name='category-by-id'),
    path('<int:nid>/', legend_by_id, name='legend-by-id'),
    path('<int:cid>/<int:nid>/', legend_by_id, name='category-legend-by-id'),
]