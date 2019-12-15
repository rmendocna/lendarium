from time import sleep

from django.core.management.base import BaseCommand, CommandError

from apl.translate import GoogleTranslator
from motif.models import Motif, Type


class Command(BaseCommand):
    help = 'Translate english Motif descriptors to Portuguese using Google Translate API'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        motifs = Motif.objects.all()
        translator = GoogleTranslator()
        failed = passed = 0
        for tom in motifs:
            if len(tom.descriptor_pt) < 3:
                try:
                    translation = translator.translate(tom.descriptor_en, 'pt', 'en')
                except Exception as e:
                    failed += 1
                    self.stderr.write('{}'.format(e))
                else:
                    if type(translation) == list and 'translatedText' in translation[0]:
                        if len(translation) > 1:
                            self.stdout.write(tom.num)
                        passed += 1
                        tom.descriptor_pt = translation[0]['translatedText']
                        tom.save()
                        self.stdout.write('.', ending='')
                sleep(.1)

        self.stdout.write('passed: {}'.format(passed))
        self.stdout.write('failed: {}'.format(failed))
