from django.utils.text import slugify as base_slugify


class SlugifyMixin(object):
    """
    requires `slug` field to be declared on the model
    """
    def _slugify(self, text, slugfield='slug'):
        _slug = base_slugify(text)
        similar = self.__class__.objects.filter(**{'{}__iregex'.format(slugfield): '^{}(?:-\d+)?$'.format(_slug)})
        cnt = similar.count()
        if cnt > 1:
            _slug += "-{:d}".format(self.id)
            print(_slug)
        return _slug
