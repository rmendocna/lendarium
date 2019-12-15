from django.apps import AppConfig

from reversion.revisions import register as reversion_register
from mptt import register as mptt_register


class ContentConfig(AppConfig):
    name = 'content'

    def ready(self):
        Article = self.get_model('Article')
        reversion_register(Article)
        mptt_register(Article)
