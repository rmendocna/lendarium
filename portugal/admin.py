from django.contrib import admin
from django.contrib.gis import admin as geoadmin

from mptt.admin import MPTTModelAdmin

from .models import Region, NUTS


class NUTSAdmin(MPTTModelAdmin):
    pass


class RegionAdmin(MPTTModelAdmin, geoadmin.OSMGeoAdmin):
    list_display = ('name', 'dicofre', 'area')
    fieldsets = (
        (None, {'fields': ('name', 'dicofre', ('area', 'outras_inf'), 'mpoly')}),
    )
    search_fields = ['name', 'parent__name']
    raw_id_fields = ('parent',)


geoadmin.site.register(Region, RegionAdmin)
admin.site.register(NUTS, NUTSAdmin)
