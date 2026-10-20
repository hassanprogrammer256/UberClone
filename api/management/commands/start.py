from django.core.management.base import BaseCommand, CommandError
from api.models import Location
import os,json

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'locations.json')

class Command(BaseCommand): 
    help = "Initialize the Locations in Uganda at the start of the App"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run',action='store_true',help='Simulate the creation of the cities in the database')

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING("=== DRY RUN MODE: No database changes will be saved ==="))

        try:
            if Location.objects.exists():
                self.stdout.write(self.style.WARNING(f"{Location.objects.count()} Locations Already Exist."))
                return

            self.stdout.write(self.style.SUCCESS("Generating Locations. Please Wait..."))

            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f"Locations JSON file not found at: {file_path}"))
                return

            self.stdout.write(self.style.SUCCESS("File Located. Processing data..."))

            with open(file_path, 'r') as f:
                locations_data = json.load(f)

                for item in locations_data:
                    name = item.get('city')
                    lat = item.get('lat')
                    long = item.get('lng')

                    if dry_run:
                        self.stdout.write(self.style.NOTICE(f"[Dry-Run] Would create location: {name} ({lat}, {long})"))
                    else:
                        Location.objects.create(
                            name=name,
                            lat=lat,
                            long=long
                        )
                        self.stdout.write(self.style.SUCCESS(f"Successfully created: {name}"))

            if dry_run:
                self.stdout.write(self.style.WARNING("=== DRY RUN COMPLETE: 0 records saved ==="))
            else:
                self.stdout.write(self.style.SUCCESS("=== OPERATION COMPLETE: Locations initialized successfully ==="))

        except Exception as e:
            raise CommandError(f"Something went wrong: {e}")
