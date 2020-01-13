from django.core.management.base import BaseCommand

from geofr.models import Perimeter


class Command(BaseCommand):
    """Import the list of all regions."""

    def handle(self, *args, **options):

        france, _ = Perimeter.objects.update_or_create(
            scale=Perimeter.TYPES.country,
            code='FRA',
            name='France')
        europe, _ = Perimeter.objects.update_or_create(
            scale=Perimeter.TYPES.continent,
            code='EU',
            name='Europe')

        PerimeterContainedIn = Perimeter.contained_in.through
        PerimeterContainedIn.objects.update_or_create(
            from_perimeter_id=france.id,
            to_perimeter_id=europe.id)
