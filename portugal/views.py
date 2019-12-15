from django.views.generic.detail import DetailView

from .models import Region


class PlaceView(DetailView):

    template_name = 'legends/place.html'
    model = Region
    pk_url_kwarg = 'pid'

