from django.db import models

from photologue.models import Photo


class ForeignPhotoField(models.ForeignKey):
    """
    A raw input field which looks up a related Photo.
    """
    def __init__(self, **kwargs):
        super(ForeignPhotoField, self).__init__(Photo, on_delete=models.PROTECT, **kwargs)


class ManyToManyPhotosField(models.ManyToManyField):

    def __init__(self, **kwargs):
        super(ManyToManyPhotosField, self).__init__(Photo, **kwargs)
