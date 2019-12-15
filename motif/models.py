from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from translated_fields.fields import TranslatedField


class Base(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT, swappable=True, editable=False,
                                 related_name='%(class)s_modified')

    class Meta:
        abstract = True


class Index(Base):
    name = models.CharField(_('Name'), unique=True, max_length=100)
    is_type = models.BooleanField(_("Is Type?"), default=True)
    description = models.CharField(_('Description'), max_length=255, blank=True)
    comments = models.TextField(_('Comments'), blank=True)
    mask = models.CharField(_('Mask'), max_length=50, blank=True)

    def __str__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = _('Index')
        verbose_name_plural = _('Indices')


class TypeOrMotif(models.Model):
    num = models.CharField(_('Num'), max_length=20, primary_key=True)
    descriptor = TranslatedField(models.TextField(_('Description'), blank=True))
    comments = models.TextField(_('Comments'), blank=True)
    # related = models.ManyToManyField('self',related_name="related_motifs",
    #    null=True,blank=True)

    def __str__(self):
        stri = "%s [%s] %s" % (getattr(self, 'index', ''), self.num, self.descriptor)
        return stri[:70]

    class Meta:
        abstract = True

class TypeOrMotifManager(models.Manager):

    def get_queryset(self):
        qs = super(TypeOrMotifManager, self).get_queryset()
        return qs.select_related('index')


class Motif(Base, TypeOrMotif):

    index = models.ForeignKey(Index, models.PROTECT, verbose_name=_('index'), limit_choices_to={'is_type': False})

    objects = TypeOrMotifManager()

    class Meta:
        verbose_name = _('Motif')


class Type(TypeOrMotif):

    index = models.ForeignKey(Index, models.PROTECT, verbose_name=_('index'), limit_choices_to={'is_type': True})

    objects = TypeOrMotifManager()

    class Meta:
        verbose_name = _('Type')

