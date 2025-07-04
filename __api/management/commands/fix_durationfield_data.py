from django.core.management.base import BaseCommand
from api.models import ManufacturePlanItem
from django.db import transaction
import datetime


class Command(BaseCommand):
    help = 'Fix invalid DurationField data in ManufacturePlanItem.average_time'

    def handle(self, *args, **options):
        invalid_items = []
        with transaction.atomic():
            for item in ManufacturePlanItem.objects.all():
                avg_time = item.average_time
                if avg_time is not None and not isinstance(avg_time, datetime.timedelta):
                    self.stdout.write(
                        f'Fixing item id={item.id} with invalid average_time={avg_time}')
                    try:
                        # Try to parse string to timedelta assuming format "HH:MM:SS"
                        parts = str(avg_time).split(':')
                        if len(parts) == 3:
                            hours, minutes, seconds = map(int, parts)
                            item.average_time = datetime.timedelta(
                                hours=hours, minutes=minutes, seconds=seconds)
                        else:
                            # If format unknown, reset to zero timedelta
                            item.average_time = datetime.timedelta(0)
                        item.save()
                    except Exception as e:
                        self.stderr.write(
                            f'Failed to fix item id={item.id}: {e}')
                        invalid_items.append(item.id)
        if invalid_items:
            self.stderr.write(f'Could not fix items with ids: {invalid_items}')
        else:
            self.stdout.write(
                'All invalid DurationField data fixed successfully.')
