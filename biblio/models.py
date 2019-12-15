from django.db import models
from django.utils.translation import ugettext_lazy as _

from translated_fields import TranslatedField


EXCERPT_TYPE_CHOICES = (
    ('pp', _('Pages')),
    ('chapter', _('Chapter')),
    ('paragraph', _('Paragraph')),
    ('part', _('Part'))
)

MEDIUM_CHOICES = (
    ('print', _('Print')),
    ('audio', _('Audio')),
    ('video', _('Video'))
)

VOLUME_TYPES = (
    ('BOOK', _('Book')),
    ('COLLECTION', _('Collection')),
    ('MAGAZINE', _('Magazine')),
    ('JOURNAL', _('Journal')),
    ('NEWSPAPER', _('Newspaper')),
    ('ARTICLE', _('Article')),
)

GENDER_CHOICES = (('M', _('Male')), ('F', _('Female')), ('-', _('Unknown/Undeclared')))


class Person(models.Model):
    first_name = models.CharField(_('First Name'), max_length=50)
    last_name = models.CharField(_('Last Name'), max_length=50)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    birth_year = models.SmallIntegerField(_("Year of Birth"), null=True, blank=True)

    def __str__(self):
        return u"%s, %s" % (self.last_name.upper(), self.first_name)

    class Meta:
        verbose_name=_("Person")


class Publisher(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    # place = models.CharField(_('Place'),max_length=255,blank=True)

    def __str__(self):
        return u"%s" % self.name


class VolumeType(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    medium = models.CharField(_('Medium type'), max_length=5, choices=MEDIUM_CHOICES, default=MEDIUM_CHOICES[0][0])


class City(models.Model):
    country = models.CharField(_('Country'), max_length=150)
    name = TranslatedField(models.CharField(_('Name'), max_length=150), {"en": {"blank": True}})

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')

    def __str__(self):
        return "%s" % self.name


class VolumeManager(models.Manager):

    def get_queryset(self):
        qs = super(VolumeManager, self).get_queryset()
        return qs.select_related('city', 'publisher', 'belongs_to').prefetch_related('authors')


class Volume(models.Model):
    """ Book, Collection, Magazine, Journal, """
    title = models.CharField(_('Title'), max_length=255)
    subtitle = models.CharField(_('Sub-Title'),max_length=255, blank=True)
    authors = models.ManyToManyField(Person, verbose_name=_("Authors"), related_name="book_authors")
    # volume_type = models.ForeignKey(VolumeType,verbose_name=_('Type'))
    type = models.CharField(_('Volume Type'), max_length=15, choices=VOLUME_TYPES, default=VOLUME_TYPES[0][0],
                            blank=True)
    editor = models.CharField(_('Editor'), max_length=255, blank=True)
    city = models.ForeignKey(City, models.PROTECT, verbose_name=_('City'), max_length=150, blank=True)
    pub_year = models.CharField(_("Year"), max_length=4, blank=True,
                                help_text="Year of publication")  # , validator_list=[validators.isOnlyDigits])
    original_year = models.CharField(_("Original Year"), max_length=4, blank=True, null=True,
                                     help_text="Year of publication of original print")
    publisher = models.ForeignKey(Publisher, models.PROTECT, verbose_name=_('Publisher'))
    belongs_to = models.ForeignKey('self', models.PROTECT, verbose_name="In",
                                   limit_choices_to={'is_collection': True}, null=True, blank=True)
    is_collection = models.BooleanField(_('Is Multiple'), default=False, editable=False)
    isbn = models.CharField('ISBN', max_length=20, blank=True)
    book_url = models.URLField(_('Book/Author web address'), blank=True, null=True)
    notes = models.TextField(_('Notes'),blank=True)
    presentation = models.CharField(_('Presentation'), max_length=10, blank=True)
    slug = models.SlugField(max_length=255, blank=False)

    objects = VolumeManager()

    def __str__(self):
        s = "%s, " % self.authorlist()
        s += "%s, " % self.fulltitle()
        s += "%s, %s, %s" % (self.city, self.publisher, self.pub_year)
        if self.original_year not in ['', None]:
            s += " [%s]" % self.original_year
        return s

    def pretty_print(self):
        s = "%s, " % self.authorlist()
        s += "<em>%s</em>, " % self.fulltitle()
        s += "%s, %s, %s" % (self.city, self.publisher, self.pub_year)
        if self.original_year not in ['', None]:
            s += " [%s]" % self.original_year
        return s
    pretty_print.alow_tags = True

    def fulltitle(self):
        s = u""
        if self.belongs_to not in ['',None]:
            s = "%s, " % self.belongs_to.title
        s += "%s" % self.title
        return s
    fulltitle.short_description = _("title(s)")

    def authorlist(self):
        s = ""
        try:
            s += "%s" % self.authors.all()[0]
            try:
                s += ", %s" % self.authors.all()[1]
                try:
                    third = "%s" % self.authors.all()[2]
                except:
                    pass
                else:
                    s += ", ET AL."  # % self.authors.all()[0]
            except:
                pass
        except:
            pass
        return s
    authorlist.short_description = _('authors')

    class Meta:
        ordering = ('title',)

    # @revision.create_on_success
    def save(self, *args, **kwargs):
        if self.type in ['COLLECTION','JOURNAL']:
            self.is_collection = True
        # revision.user = threadlocals.get_current_user()
        super(Volume, self).save(*args, **kwargs)


class Citation(models.Model):
    """This class gathers complex citation information
    """
    book = models.ForeignKey(Volume, models.PROTECT, verbose_name=_('Volume'))
    description = models.CharField(_('Excerpt'), max_length=255, blank=True,
                                   help_text=_('Part, chaper, passage, page, etc..'))

# class Update(models.Model):
#    headline = models.CharField(max_length=255,)
#    pub_date = models.DateTimeField('date published', auto_now_add=True)
#    book = models.ForeignKey(Book, edit_inline=models.TABULAR, num_in_admin=3)
#    def __str__(self):
#        return self.headline
#    class Admin:
#        fields = (
#            (None, {
#            'fields': ('book', 'headline')}),
#            )
#        list_display = ('headline', 'book', 'pub_date')
