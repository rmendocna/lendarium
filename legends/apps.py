from django.apps import AppConfig

from reversion.revisions import register as reversion_register
from mptt import register as mptt_register


class LegendsConfig(AppConfig):
    name = 'legends'

    def ready(self):
        Category = self.get_model('Category')
        Narrative = self.get_model('Narrative')
        reversion_register(Category)
        reversion_register(Narrative)
        mptt_register(Category)

