from time import sleep

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from apl.translate import GoogleTranslator
from legends.models import Narrative


class Command(BaseCommand):
    help = 'Translate english Motif descriptors to Portuguese using Google Translate API'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        narratives = Narrative.objects.filter(Q(common_title_en='--') | Q(common_title_en=''))
        translator = GoogleTranslator()
        failed = passed = 0
        for narr in narratives:
            title = narr.common_title_pt
            if title.strip() == '--' or not title:
                title == narr.title.strip()
            try:
                translation = translator.translate(title, 'en', 'pt')
            except Exception as e:
                failed += 1
                self.stderr.write('{}'.format(e))
            else:
                if type(translation) == list and 'translatedText' in translation[0]:
                    if len(translation) > 1:
                        self.stdout.write(narr.num)
                    passed += 1
                    narr.common_title_en = translation[0]['translatedText']
                    narr.save(dismiss_analytics=True, redo_slugs=True)

        self.stdout.write('passed: {}'.format(passed))
        self.stdout.write('failed: {}'.format(failed))
