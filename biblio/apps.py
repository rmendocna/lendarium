from django.apps import AppConfig

from reversion.revisions import register


class BiblioConfig(AppConfig):
    name = 'biblio'

    def ready(self):
        Person = self.get_model('Person')
        Publisher = self.get_model('Publisher')
        VolumeType = self.get_model('VolumeType')
        City = self.get_model('City')
        Volume = self.get_model('Volume')
        register(Person)
        register(Publisher)
        register(VolumeType)
        register(City)
        register(Volume)
