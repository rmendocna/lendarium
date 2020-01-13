from django.contrib.gis.db import models as gis_models
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

import mptt
from mptt.models import MPTTModel, TreeForeignKey


class NUTS(MPTTModel):
    designacao = models.CharField(max_length=64, blank=True)
    code = models.CharField(max_length=2, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return "%s" % self.designacao

    class Meta:
        verbose_name_plural = "NUTS"
        ordering = ['lft']

    class MPTTMeta:
        order_insertion_by = ['designacao']


class Region(gis_models.Model):
    dicofre = models.CharField(_('DiCoPar'), max_length=6)
    name = models.CharField(_('Parish'), max_length=100)
    outras_inf = models.CharField(_('Other Info.'), max_length=255, blank=True)
    area = models.FloatField(_('Area'), null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    mpoly = gis_models.MultiPolygonField(null=True, blank=True)

    nuts = models.ForeignKey(NUTS, models.PROTECT, null=True, verbose_name="NUTS", blank=True)
    # objects = gis_models.GeoManager()

    def get_distrito(self):
        if self.parent_id:
            return self.get_ancestors().first()
        else:
            return self
    get_distrito.short_description = _('District')

    @property
    def distrito(self):
        return self.get_distrito().name
    # distrito.short_description = _('District')

    @property
    def concelho(self):
        if self.parent_id:
            return self.parent.name
        return ''

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")
        ordering = ['lft']
        # order_with_respect_to = 'concelho'

    def __str__(self):
        if self.parent_id:
            return "%s (%s)" % (self.name, self.parent.name)
        elif self.name:
            return self.name
        else:
            return ''

    # @models.permalink
    def get_absolute_url(self):
        return reverse('place', kwargs=dict(pid=str(self.id)))

    def pretty_print(self):
        lst = ['<a href="{}">{}</a>'.format(self.get_absolute_url(), self.name)]
        if self.parent_id:
            parent = self.parent
            if parent.parent_id:
                lst += ['<a href="{}">{}</a>'.format(parent.get_absolute_url(), parent.name)]
                parent = parent.parent
            lst += [parent.name]
        return ', '.join(lst)
    pretty_print.allow_tags = True


try:
    mptt.register(Region, order_insertion_by=['name'])
except:
    pass
