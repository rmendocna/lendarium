from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mptt.admin import DraggableMPTTAdmin
from reversion.admin import VersionAdmin
from .models import (Bibliography, Category, Name, Narrative, NarrativeType, NarrativeVersion,
                     Person, Place, Url)  # NarrativeMotif,


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'sex', 'age')
    search_fields = ('first_name', 'last_name')

    fieldsets = (
        (None, {'fields': (('first_name', 'last_name'), ('sex', 'birth_year', 'age'), 'birthplace', 'residence')}),
    )
    radio_fields = {'sex': admin.HORIZONTAL}
    raw_id_fields = ('birthplace', 'residence')

    def save_model(self, request, obj, form, change):
        obj.modifier = request.user
        obj.save()


# class MotifInline(admin.TabularInline):
#     model = NarrativeMotif
#     extra = 3
#     raw_id_fields = ('motif', )


class TypeInline(admin.TabularInline):
    model = NarrativeType
    extra = 3
    raw_id_fields = ('type', )


class VersionInline(admin.TabularInline):
    model = NarrativeVersion
    fk_name = 'narrative'
    extra = 3
    raw_id_fields = ('version', )


class BibliographyInline(admin.TabularInline):
    model = Bibliography
    extra = 3


class PlaceInline(admin.TabularInline):
    model = Place
    extra = 3
    raw_id_fields = ('place', )


@admin.register(Narrative)
class NarrativeAdmin(VersionAdmin):
    list_display = ('title', 'collection_place')
    search_fields = ('title', *Narrative.common_title.fields)
    filter_horizontal = ['motifs', 'categories']
    fieldsets = (
        (_('collection'), {
            'classes': ['collapse'],
            'fields': (('citation', 'excerpt'), ('collection_place', 'collection_year'), ('informant', 'collector'), )
        }),
        (_('Narrative'), {
            'classes': ['collapse'],
            'fields': (('year_narrative', 'date_century', 'date_decade'), ('belief', 'presentation'))
        }),
        (_('Analysis'), {
            'classes': ['collapse'],
            'fields': ('categories', 'notes')
        }),
        (None, {
            'fields': (('title', 'version_number'), 'transcription', ('most_frequent', 'names', 'places'),
                       'other_title'),
        }),
        (_('References'), {
            'classes': ['collapse'],
            'fields': ('web_references', 'other', 'motifs')
        }),
    )
    inlines = [TypeInline, PlaceInline] # , BibliographyInline, VersionInline,
    # autocomplete_fields = ['motifs', 'narratives']
    raw_id_fields = ['citation', 'collector', 'informant', 'collection_place']
    list_select_related = ('citation', 'collection_place', 'collection_place__parent')


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title',)


admin.site.register(Name)
admin.site.register(Url)

