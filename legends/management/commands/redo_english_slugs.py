from django.core.management.base import BaseCommand

from legends.models import Narrative


class Command(BaseCommand):
    help = 'iRedo english slugs'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        narratives = Narrative.objects.all()  # filter(common_title_pt__startswith='-')
        blanks = 0
        for narr in narratives:
            title = narr.common_title_pt
            self.stdout.write(narr.common_title_pt, ending=' ** ')
            self.stdout.write(narr.common_title_en)
        #     if not title or title.startswith('-'):
        #         blanks += 1
        #         continue
        #     title = title.replace('[', ' ').replace(']', ' ')
        #     narr.slug_en = narr._slugify(title.strip(), slugfield='slug_en')
        #     narr.save(dismiss_analytics=True, redo_slugs=False)
        #
        # self.stdout.write('Narratives: {}'.format(narratives.count()))
        # self.stdout.write('Blanks: {}'.format(blanks))
