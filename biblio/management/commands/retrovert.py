import json
from django.apps.registry import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

LANGS = [k for k, v in settings.LANGUAGES]


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--json', type=str)

    def handle(self, *args, **options):
        with open(options['json']) as f:
            records = json.load(f)
        modelname = None
        Model = None
        field_names = []
        for rec in records:
            if not rec['model'].endswith('translation'):
                continue
            if rec['model'] != "{}translation".format(modelname):
                modelname = rec['model']
                _app, _model = modelname.split('.')
                _model = _model.replace('translation', '')
                Model = apps.get_model(_app, _model)
                field_names = [f.name for f in Model._meta.get_fields() if '_' in f.name]
            all_fields = rec['fields']
            obj = Model.objects.get(pk=all_fields['master'])
            flds = set(all_fields.keys()) - {'master', 'language_id'}
            lidx = int(all_fields['language_id']) - 1
            for fld in list(flds):
                fname = "%s_%s" % (fld, LANGS[lidx])
                if fname in field_names:
                    setattr(obj, fname, all_fields[fld])
                else:
                    setattr(obj, fld, all_fields[fld])
            obj.save()
            self.stdout.write('.', ending='')

