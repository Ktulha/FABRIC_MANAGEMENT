from django.core.management.base import BaseCommand, CommandError
from django.apps import apps


class Command(BaseCommand):
    help = 'Clear all records from the specified table (model) in the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            'model', type=str, help='Model name in the format app_label.ModelName')

    def handle(self, *args, **options):
        model_name = options['model']
        try:
            app_label, model_class_name = model_name.split('.')
        except ValueError:
            raise CommandError(
                'Model name must be in the format app_label.ModelName')

        model = apps.get_model(app_label, model_class_name)
        if model is None:
            raise CommandError(f'Model "{model_name}" not found.')

        count, _ = model.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            f'Successfully deleted {count} records from {model_name}.'))
