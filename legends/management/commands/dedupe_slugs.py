from django.core.management.base import BaseCommand
from django.db.models import Q

from legends.models import Narrative


class Command(BaseCommand):
    help = 'Translate english Motif descriptors to Portuguese using Google Translate API'

    def handle(self, *args, **options):
        mx = 3
        while mx > 2:
            found = False
            narratives = Narrative.objects.filter(Q(slug_en__endswith='-1') | Q(slug_pt__endswith='-1')
                                                  ).values('slug_en', 'slug_pt').distinct()
            for narr in narratives:
                sum = Narrative.objects.filter(slug_en=narr.slug_en).count()
                if sum > 1:
                    slg = narr.slug_en[:-1]
                    narr.slug_en = "{}{}".format(slg, sum)
                    if sum > mx:
                        mx = sum
                    found = True
                    self.stdout.write('E', ending='')

                sum = Narrative.objects.filter(slug_pt=narr.slug_pt).count()
                if sum > 1:
                    slg = narr.slug_pt[:-1]
                    narr.slug_pt = "{}{}".format(slg, sum)
                    if sum > mx:
                        mx = sum
                    found = True
                    self.stdout.write('P', ending='')
                if found:
                    narr.save()
                    self.stdout.write('{}'.format(mx), ending='')

