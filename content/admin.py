from datetime import date

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from mptt.admin import DraggableMPTTAdmin
from reversion.admin import VersionAdmin
from reversion.models import Version
from translated_fields import TranslatedFieldAdmin

from .models import Article


@admin.register(Article)
class ArticleAdmin(DraggableMPTTAdmin, VersionAdmin, TranslatedFieldAdmin):
    list_display = ('tree_actions', 'indented', 'last_edited', 'is_public')
    list_display_links = ('indented',)
    fieldsets = (
        ('', {'fields': (('is_public', 'date_pub'),
                         tuple(Article.title.fields), tuple(Article.short_title.fields),
                         *Article.text.fields, tuple(Article.keywords.fields),
                         ('menu', 'parent'),
                         tuple(Article.slug.fields),
                         )}
         ),
    )

    readonly_fields = tuple(Article.slug.fields)

    history_latest_first = True

    def indented(self, inst):
        return format_html('<div style="text-indent:{}px">{}</div>', inst._mpttfield('level') * self.mptt_level_indent,
                           inst.title)
    indented.short_description = _('title')
    indented.allow_tags = True

    def is_public(self, instance):
        return instance.date_pub <= date.today() or self.is_public
    is_public.boolean = True

    def last_edited(self, instance):
        versions = Version.objects.get_for_object(instance)
        if versions.exists():
            version = versions.first()
            out = version.revision.date_created
        else:
            out = ''
        return out
