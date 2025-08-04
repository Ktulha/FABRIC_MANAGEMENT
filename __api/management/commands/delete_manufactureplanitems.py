from django.core.management.base import BaseCommand
from api.models import ManufacturePlanItem


class Command(BaseCommand):
    help = 'Delete all data from ManufacturePlanItem table'

    def handle(self, *args, **options):
        count, _ = ManufacturePlanItem.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            f'Successfully deleted {count} items from ManufacturePlanItem table.'))
