from datetime import date

from django.conf import settings
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey
from tagging.fields import TagField
from tinymce.models import HTMLField
from translated_fields import TranslatedField

from apl.utils import get_marked, most_frequent
from apl.models import SlugifyMixin

LANG_PREFIXES = list(zip(*settings.LANGUAGES))[0]

GENDER_CHOICES = (('M', _('Male')), ('F', _('Female')), ('-', _('Unknown')))

SECULOS = (
    (-20, 'XX ac'), (-19, 'IXX ac'), (-18, 'XVIII ac'), (-17, 'XVII ac'), (-16, 'XVI ac'),
    (-15, 'XV ac'), (-14, 'XIV ac'), (-13, 'XIII ac'), (-12, 'XII ac'), (-11, 'XI ac'),
    (-10, 'X ac'), (-9, 'IX ac'), (-8, 'VIII ac'), (-7, 'VII ac'), (-6, 'VI ac'), (-5, 'V ac'),
    (-4, 'IV ac'), (-3, 'III ac'), (-2, 'II ac'), (-1, 'I ac'), (1, 'I'), (2, 'II'), (3, 'III'),
    (4, 'IV'), (5, 'V'), (6, 'VI'), (7, 'VII'), (8, 'VIII'), (9, 'IX'), (10, 'X'), (11, 'XI'),
    (12, 'XII'), (13, 'XIII'), (14, 'XIV'), (15, 'XV'), (16, 'XVI'), (17, 'XVII'), (18, 'XVIII'),
    (19, 'XIX'), (20, 'XX'), (21, 'XXI')
)

decs = range(0, 100, 10)
sdecs = [(str(d)+"s") for d in decs]
DECADES = tuple(zip(decs, sdecs))

BELIEF_CHOICES = (
    (1, _('Convinced Disbelief')),
    (2, _('Some Scepticism')),
    (3, _('Unsure / Uncommitted')),
    (4, _('Some Belief')),
    (5, _('Convinced Belief'))
)

PRESENTATION_CHOICES = (
    (5, _('Oral transcription')),
    (4, _('Memory transcription')),
    (3, _('Scientific written text')),
    (2, _('Citation/Quote')),
    (1, _('Ludic written text'))
)


class Base(models.Model):
    created = models.DateTimeField(editable=False, auto_now_add=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, editable=False,
                                related_name='%(class)s_creator')
    modified = models.DateTimeField(editable=False, auto_now=True)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, editable=False,
                                 related_name='%(class)s_modifier')

    class Meta:
        abstract = True


class Name(Base):
    """
    Tratando-se de uma personagem lendaria ou de uma pessoa efectiva,
    tera sempre um 'Primeiro Nome'.
    """
    first_name = models.CharField(_('First Name'), max_length=50)
    last_name = models.CharField(_('Last Name'), max_length=50, blank=True)

    def __str__(self):
        return ("%s %s" % (self.first_name, self.last_name)).strip()

    class Meta:
        verbose_name = _("Name")


class Person(Name):
    sex = models.CharField(_('Gender'), max_length=1, choices=GENDER_CHOICES)
    birth_year = models.SmallIntegerField(_("Year of Birth"), null=True, blank=True)
    age = models.SmallIntegerField(_("Age"), null=True, blank=True)
    birthplace = models.ForeignKey('portugal.Region', on_delete=models.PROTECT, verbose_name=_("Place of birth"),
                                   related_name="babies", null=True, blank=True)
    residence = models.ForeignKey('portugal.Region', on_delete=models.PROTECT, verbose_name=_("Place of residence"),
                                  related_name="residents", null=True, blank=True)
    notes = models.CharField(_('Notes'), max_length=255, blank=True,
                             help_text=_('Contacts, Education, Learned from..., '))

    def calculated_age(self):
        if self.birth_year:
            return "%d" % (date.today().year-self.birth_year)
        else:
            return "-"
    calculated_age.short_description = _('age (today)')

    class Meta:
        verbose_name = _("Person")


class Category(MPTTModel, SlugifyMixin, Base):
    """
    Categories are hierarchical. Consider having weighed relationships between them.
    Expected categories include 'Holy/Sacred', 'Urban/Contemporary',
    'Holy->Christian", "Holy->Christian->Catholic'.
    """
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                            verbose_name=_('Is a sub-category of'), related_name='child_categories')
    name = TranslatedField(models.CharField(_('Name'), max_length=50, blank=True))
    description = TranslatedField(models.CharField(_('Description'), max_length=255, blank=True),
                                  {"en": {"blank": True}})
    slug = TranslatedField(models.SlugField(_('slug'), max_length=53, blank=True))

    def __str__(self):
        the_name = u""
        if self.parent:
            the_name = u"%s :: " % self.parent
        return u"%s%s" % (the_name, self.name)

    def get_absolute_url(self):
        url = reverse('category-detail', kwargs={'slug': self.slug})
        return url

    def save(self, *args, **kwargs):
        for lng in LANG_PREFIXES:
            slug_field = 'slug_{}'.format(lng)
            slug = getattr(self, slug_field, '')
            if not slug:
                name = getattr(self, 'name_{}'.format(lng), '')
            setattr(self, slug_field, self._slugify(name, slugfield=slug_field))
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Url(models.Model):
    address = models.URLField(_('Web Reference'),
                              help_text=_('It should start with a \'http://\' and contain no spaces.'))

    def __str__(self):
        return u"%s" % self.address

    class Meta:
        verbose_name = "URL"


class NarrativeManager(models.Manager):

    def get_queryset(self):
        qs = super(NarrativeManager, self).get_queryset()
        return qs.prefetch_related('motifs', 'narrativetype_related', 'citation__authors').select_related(
            'informant', 'collection_place', 'collection_place__parent', 'collection_place__parent',
            'citation', 'citation__city', 'citation__publisher')


class Narrative(SlugifyMixin, Base):
    is_public = models.BooleanField(_('Is public?'), default=True, )
    version_number = models.IntegerField(_('Version Number'), null=True, blank=True, help_text=_('Deprecated'))
    title = models.CharField(_('Title'), max_length=255)
    other_title = models.CharField(_('Support Title'), max_length=255, null=True, blank=True)
    # collection
    citation = models.ForeignKey('biblio.Volume', on_delete=models.PROTECT, verbose_name=_("Biblio. Ref."), null=True,
                                 blank=True, related_name="citations", limit_choices_to={"is_collection__exact": False},
                                 help_text=_("Filling this will excuse you from filling the remaining fields of this group."))
    excerpt = models.CharField(_('Excerpt'), max_length=255, blank=True,
                               help_text=_('Part, chaper, passage, page, etc..'))
    collection_year = models.IntegerField(_('Year'), null=True, blank=True)
    collection_place = models.ForeignKey('portugal.Region', on_delete=models.PROTECT, verbose_name=_('Place'), null=True,
                                         blank=True, related_name='collections')
    collector = models.ForeignKey(Person, on_delete=models.PROTECT, verbose_name=_('Collector'), null=True,
                                  blank=True, related_name='collectors')
    informant = models.ForeignKey(Person, on_delete=models.PROTECT, verbose_name=_('Informant'), null=True,
                                  blank=True, related_name='informants')
    transcription = HTMLField(_('Transcription'), blank=True)
    most_frequent = TagField(verbose_name=_('Most Frequent'), blank=True,
                             help_text=_('(Most frequent single words. You should let *me* fill this in. Thank you.)'))
    places = TagField(verbose_name=_('Places'), blank=True)
    names = TagField(verbose_name=_('Names'), blank=True)
    # audio = FileBrowseField('Audio', max_length=250, blank=True, null = True,
    #                         directory="audio/", extensions=['.mp3', ])
    # attach = FileBrowseField(_('Attachment'), max_length=250, blank=True, null = True,
    #                          directory="attachs/", extensions=['.mp3', ])

    # narrative
    year_narrative = models.SmallIntegerField(_('Year'), null=True, blank=True)
    date_century = models.SmallIntegerField(_('Century'), choices=SECULOS, default=20, null=True, blank=True)
    date_decade = models.SmallIntegerField(_('Decade'), choices=DECADES, default=90, null=True, blank=True)
    presentation = models.SmallIntegerField(_('Presentation'), choices=PRESENTATION_CHOICES,
                                            default=PRESENTATION_CHOICES[2][0])
    belief = models.SmallIntegerField(_('Belief'), choices=BELIEF_CHOICES, default=3,
                                      null=True, blank=True)
    rating = models.IntegerField(_('Rating'), editable=False, default=0)
    notes = models.TextField(_('Comments'), blank=True)
    # references
    web_references = models.ManyToManyField(Url, verbose_name=_('Web references'), blank=True)
    other = models.TextField(_('Other References'), null=True, blank=True)
    ##
    categories = models.ManyToManyField(Category, verbose_name=_('Categories'), blank=True)
    narratives = models.ManyToManyField('self', verbose_name=_('Related Narratives'), symmetrical=False,
                                        through='NarrativeVersion', related_name='related_narratives')
    many_places = models.ManyToManyField('portugal.Region', verbose_name=_('Counties/Parishes'),
                                         help_text=_('Help us putting it on the map!'), blank=True, )
    many_names = models.ManyToManyField(Name, help_text=_('Names occurring or referred to in the Text'))

    common_title = TranslatedField(models.CharField(_('Common title'), max_length=255, blank=True))
    slug = TranslatedField(models.CharField(max_length=255, editable=False, db_index=True, blank=True))
    abstract = TranslatedField(HTMLField(_('Abstract'), blank=True))
    keywords = TranslatedField(TagField(verbose_name=_('Keywords'), blank=True,
                                        help_text=_("Separate with commas. Will be converted to lowercase.")))
    motifs = models.ManyToManyField('motif.Motif')  # through='NarrativeMotif'

    objects = NarrativeManager()

    def save(self, *args, **kwargs):
        dismiss_analytics = kwargs.pop('dismiss_analytics', False)
        redo_slugs = kwargs.pop('redo_slugs', False)
        for lng in LANG_PREFIXES:
            title_field = 'title_{}'.format(lng)
            title = getattr(self, title_field, '').strip()
            setattr(self, title_field, title)
            slug_field = 'slug_{}'.format(lng)
            slug = getattr(self, slug_field, '')
            if not slug or redo_slugs:
                common_title = getattr(self, 'common_title_{}'.format(lng), '') or title
                setattr(self, slug_field, self._slugify(common_title, slugfield=slug_field))
        if not dismiss_analytics:
            self.places = get_marked(self.transcription, 'places')
            self.names = get_marked(self.transcription, 'names')
            mf = most_frequent(self.transcription)
            self.most_frequent = ", ".join(mf)
        super(Narrative, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('narrative-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _("Narrative")
        ordering = [Lower('title')]


# class NarrativeMotif(Base):
#     narrative = models.ForeignKey(Narrative, on_delete=models.PROTECT, verbose_name=_("Record"),
#                                   related_name="%(class)s_related")
#     motif = models.ForeignKey('motif.Motif', on_delete=models.PROTECT, verbose_name=_("Motif"),
#                               related_name="motif_related")
#
#     def __str__(self):
#         return "%s"[:60] % self.motif
#
#     class Meta:
#         verbose_name = _("Related Motif")
#         verbose_name_plural = _('Related Motifs')
#         # db_table = 'legends_narrative_motifs'


class NarrativeType(models.Model):
    narrative = models.ForeignKey(Narrative, on_delete=models.PROTECT, verbose_name=_("Record"),
                                  related_name="%(class)s_related")
    type = models.ForeignKey('motif.Type', on_delete=models.PROTECT, verbose_name=_("Type"),
                             related_name="type_related")

    def __str__(self):
        return "%s"[:60] % self.type

    class Meta:
        verbose_name = _("Related Type")
        verbose_name_plural = _('Related Types')


class Place(Base):
    narrative = models.ForeignKey(Narrative, on_delete=models.PROTECT, verbose_name=_("Record"),
                                  related_name="%(class)s_related")
    place = models.ForeignKey('portugal.Region', on_delete=models.PROTECT, verbose_name=_("Place"),
                              related_name="place_related")

    class Meta:
        verbose_name = _("Related Place")
        verbose_name_plural = _('Related Places')


class NarrativeVersion(models.Model):
    narrative = models.OneToOneField(Narrative, on_delete=models.PROTECT, verbose_name=_("Record"),
                                     related_name="%(class)s_related")
    version = models.ForeignKey(Narrative, on_delete=models.PROTECT, verbose_name=_("Related Version"),
                                related_name="version_narrative_related")
    strength = models.PositiveSmallIntegerField(_('Strength'), default=1)
    nature = models.CharField(_('Nature'), max_length=25, blank=True)

    def __str__(self):
        return self.version.title

    def get_absolute_url(self):
        return u"%u" % self.version.get_absolute_url()

    class Meta:
        unique_together = ('narrative', 'version', 'nature', 'strength')
        verbose_name = _("Related Narrative")
        verbose_name_plural = _('Related Narratives')


class NarrativeCategory(models.Model):
    narrative = models.ForeignKey(Narrative, on_delete=models.PROTECT, verbose_name=_("Record"),
                                  related_name="%(class)s_related")
    legendcategory = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_("Related Category"),
                                       related_name="narrative_categories")


class Bibliography(models.Model):
    narrative = models.ForeignKey(Narrative, on_delete=models.PROTECT, verbose_name=_("Record"),
                                  related_name="%(class)s_related")
    reference = models.ForeignKey('biblio.Volume', on_delete=models.PROTECT, verbose_name="Volume",
                                  limit_choices_to={"is_collection__exact": False})
    excerpt = models.CharField(_('Excerpt'), max_length=30, blank=True,
                               help_text=_('Part, passage, chapter, page(s), lines, etc.., '))
    is_rewrite = models.BooleanField(_('Is a rewrite?'), default=False)
