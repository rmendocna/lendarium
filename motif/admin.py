from django.contrib import admin

from .models import Motif, Type, Index

admin.site.register(Index)


@admin.register(Motif)
class MotifAdmin(admin.ModelAdmin):
    search_fields = Motif.descriptor.fields


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    search_fields = Type.descriptor.fields
