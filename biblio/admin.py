from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import City, Person, Publisher, Volume


admin.site.register(City)
admin.site.register(Person)
admin.site.register(Publisher)


@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('belongs_to', 'title', 'subtitle', 'authors', ('publisher', 'city', 'isbn'),
                       ('pub_year', 'original_year'))
        }),
        (_('Extra info'), {'fields': ('type', ('editor', 'book_url'), 'notes',)}),
    )
    list_display = ('fulltitle', 'authorlist', 'publisher', 'pub_year', 'is_collection')
    search_fields = ('title', 'author')
    filter_horizontal = ('authors',)
