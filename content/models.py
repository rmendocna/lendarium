from datetime import date

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey
from tagging.fields import TagField
from tinymce.models import HTMLField
from translated_fields.fields import TranslatedField

from apl.models import SlugifyMixin


MENU_CHOICES = (
    ('top', _('Top')),
    ('bottom', _('Bottom')),
)


class PublicManager(models.Manager):

    def public(self):
        return super().get_queryset().filter(is_public=True)


class Article(MPTTModel, SlugifyMixin, models.Model):
    title = TranslatedField(models.CharField(_('title'), max_length=128))
    short_title = TranslatedField(models.CharField(_('short title'), max_length=50, blank=True,
                                  help_text=_("On the menus. Defaults to max of 3 words")))
    text = TranslatedField(HTMLField(_('text'), blank=True))
    keywords = TranslatedField(TagField(_('keywords'), max_length=255, blank=True))
    slug = TranslatedField(models.CharField(max_length=192, blank=True, db_index=True))  # , editable=False
    parent = TreeForeignKey('self', on_delete=models.PROTECT, verbose_name=_("Ancestor"), related_name='children',
                            null=True, blank=True)
    menu = models.CharField(_("Menu"), max_length=1, blank=True, choices=MENU_CHOICES)
    # images = ManyToManyPhotosField(verbose_name=_("Images"), null=True, blank=True, related_name='articles')
    is_public = models.BooleanField(_('publish'), default=True,
                                    help_text=_('public articles will be made visible on the website'))
    date_pub = models.DateField(_('publication date'), auto_created=True, blank=True)

    def save(self, *args, **kwargs):
        _cls = self.__class__
        suffixes = map(lambda x: x[-3:], _cls.title.fields)
        if not self.pk:
            for suffix in suffixes:
                slug = 'slug{}'.format(suffix)
                if not getattr(self, slug, ''):
                    title = getattr(self, 'title{}'.format(suffix))
                    setattr(self, slug, self._slugify(title, slugfield=slug))
        if not self.date_pub:
            self.date_pub = date.today()
        for suffix in suffixes:
            short = 'short_title{}'.format(suffix)
            if not getattr(self, short, ''):
                title = getattr(self, 'title{}'.format(suffix))
                setattr(self, short, ' '.join(title.split()[:2]))
        super(Article, self).save(*args, **kwargs)

    objects = PublicManager()

    def public_children(self):
        return self.get_children().filter(is_public=True).exclude(Q(title="") | Q(title__isnull=True))

    class Meta:
        verbose_name = _("Content")

    def get_absolute_url(self):
        return reverse('article-slug', kwargs={'slug': self.slug})
