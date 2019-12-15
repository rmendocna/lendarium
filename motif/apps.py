from django.apps import AppConfig

from reversion.revisions import register


class MotifConfig(AppConfig):
    name = 'motif'

    def ready(self):
        Index = self.get_model('Index')
        Motif = self.get_model('Motif')
        Type = self.get_model('Type')
        register(Motif)
        register(Index)
        register(Type)


