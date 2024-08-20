import requests
from django.core.management.base import BaseCommand
from quran.models import Juz

class Command(BaseCommand):
    help = "Fetch Quran Juzs and store them in the database."

    def handle(self, *args, **kwargs):
        response = requests.get("https://api.quran.com/api/v4/juzs")
        if response.status_code == 200:
            juzs = response.json().get("juzs", [])
            for juz_data in juzs:
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

            self.stdout.write(self.style.SUCCESS("Juzs stored successfully."))
        else:
            self.stdout.write(self.style.ERROR("Failed to fetch Juz data."))
