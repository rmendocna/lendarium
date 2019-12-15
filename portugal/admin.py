from django.contrib import admin
from django.contrib.gis import admin as geoadmin

from mptt.admin import MPTTModelAdmin

from .models import Region, NUTS  # Concelho, Distrito


class NUTSAdmin(MPTTModelAdmin):
    pass


class RegionAdmin(MPTTModelAdmin, geoadmin.OSMGeoAdmin):
    # list_display = ('name', 'level', 'area')
    # list_display_links = ('name',)
    # list_select_related = True
    fieldsets = (
        (None, {'fields': ('name', 'dicofre', ('area', 'outras_inf'), 'mpoly')}),
    )
    search_fields = ['name', 'parent__name']
    raw_id_fields = ('parent',)


# class ConcelhoAdmin(geoadmin.OSMGeoAdmin):
#     list_display = ('name', 'distrito', 'nutsiii', 'nuts_code', 'area')
#     raw_id_fields = ['distrito', 'nutsiii']
#     fieldsets = (
#         (None, {'fields': ('name', ('distrito', 'nutsiii'), ('dico', 'nuts'), 'area', 'mpoly')}),
#     )


geoadmin.site.register(Region, RegionAdmin)
# geoadmin.site.register(Concelho, ConcelhoAdmin)
# admin.site.register(Distrito)
admin.site.register(NUTS, NUTSAdmin)
