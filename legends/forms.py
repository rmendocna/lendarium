from django import forms
from django.utils.translation import ugettext as _
from wtform.forms import WTForm, Columns, Fieldset
#from django.conf import settings
from widgets import JQueryAutoComplete
import models
from motif import models as motif_models

class SearchForm(WTForm):
    apl = forms.IntegerField(label = 'APL', min_value=1, help_text=_('Specific narrative'),
                required=False,)
    title = forms.CharField(label = _('Title'), widget=JQueryAutoComplete('/xhr/narrative_titles/',attrs={'size':40}), 
                required=False, help_text = _('As complete as you can') )
    keyword = forms.CharField(label = _('Keyword'), widget=JQueryAutoComplete('/xhr/keyword/', attrs={'size':18}),
                required=False, )
                    
    place = forms.CharField(label=_('Place'), widget=JQueryAutoComplete('/xhr/source_places/',attrs={'size':40}), required=False)
    has_sound = forms.BooleanField(label=_('Audio capture'), required=False)
    collection_author = forms.CharField(label = _('Author(s)'), widget=JQueryAutoComplete('/xhr/source_authors/',attrs={'size':45}), required=False)
    collection_title = forms.CharField(label = _('Title'), widget=JQueryAutoComplete('/xhr/source_titles/', attrs={'size':60}), required=False)
    collection_year = forms.CharField(label = _('Year'), widget=forms.TextInput(attrs={'size':5}),required=False, help_text='Public.')
    belief = forms.ChoiceField(label=_('Belief'), choices = (('','--'),)+models.BELIEF_CHOICES, required=False)
    presentation = forms.ChoiceField(label=_('Presentation'), choices = (('','--'),)+ models.PRESENTATION_CHOICES, required=False)
    type = forms.ModelChoiceField(queryset=motif_models.Type.objects.filter(type_related__pk__isnull=False).distinct(), label=_("Type"), required=False)
    #types = forms.CharField(label = _('Type(s)'), help_text=_("Separate with commas"), required=False,)
    motif = forms.ModelChoiceField(queryset=motif_models.Motif.objects.filter(motif_related__pk__isnull=False).distinct(), label=_("Motif"), required=False)
    #motifs = forms.CharField(label = _('Motif(s)'), help_text=_("Separate with commas"), required=False,)
    
    class Meta:
        layout = (
            Columns(('title','place'),('keyword','has_sound'),css_class="yui-gc"),
            Fieldset(_('Publications'),Columns(('collection_author','collection_title'),('collection_year',),css_class="yui-ge")),
            Columns(('belief',),('presentation',)),
            Fieldset(_('Classifications'),Columns(#('type_index','motif_index'),
              ('type','motif',),#css_class="yui-gf"
              )),
            Columns(('apl',),css_class="yui-ge"),
            )
    
    #class Media:
    #    css = {'all': ('css/jquery.autocomplete.css',) }
    #    js = (
    #      'js/jquery-autocomplete/lib/jquery.js',
    #      'js/jquery-autocomplete/lib/jquery.bgiframe.min.js',
    #      'js/jquery-autocomplete/lib/jquery.ajaxQueue.js',
    #      'js/jquery-autocomplete/jquery.autocomplete.min.js'
    #      )

    def clean(self):
        cleaned_data = self.cleaned_data
        if len(cleaned_data)==0:
            raise _("You must fill-in at least one look-up field")
        return cleaned_data
    