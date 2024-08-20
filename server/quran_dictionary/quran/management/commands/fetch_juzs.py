import requests
from django.core.management.base import BaseCommand
from quran.models import Juz
from django.db import transaction, IntegrityError

class Command(BaseCommand):
    help = "Fetch Quran Juz and store them in the database."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Fetching Juz data..."))

        try:
            response = requests.get("https://api.quran.com/api/v4/juzs")
            response.raise_for_status()  # Raise an HTTPError for bad responses
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Failed to fetch Juz data: {e}"))
            return
        
        self.stdout.write(self.style.NOTICE("Successfully fetched Juz data."))
        juz_data_list = response.json().get("juzs", [])

        # Use a transaction to ensure atomic operations
        with transaction.atomic():
            for juz_data in juz_data_list:
                try:
                    Juz.objects.update_or_create(
                        id=juz_data["id"], 
                        defaults={
                            "juz_number": juz_data["juz_number"],
                            "first_verse_id": juz_data["first_verse_id"],
                            "last_verse_id": juz_data["last_verse_id"],
                            "verses_count": juz_data["verses_count"],
                            "verse_mapping": juz_data["verse_mapping"],
                        }
                    )
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f"IntegrityError occurred: {e}"))
                    # Optionally, log the error or handle it according to your needs
                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f"KeyError occurred: Missing key {e} in the data."))
                    # Optionally, log the missing key or handle it according to your needs

        self.stdout.write(self.style.SUCCESS("Juz stored successfully."))
