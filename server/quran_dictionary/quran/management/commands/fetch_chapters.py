import requests
from django.core.management.base import BaseCommand
from quran.models import Chapter

class Command(BaseCommand):
    help = "Fetch Quran chapters and store them in the database."

    def handle(self, *args, **kwargs):
        chapter_ids = range(1, 115)  # Chapters 1 to 114
        for chapter_id in chapter_ids:
            response = requests.get(f"https://api.quran.com/api/v4/chapters/{chapter_id}")
            if response.status_code == 200:
                data = response.json().get("chapter", {})
                Chapter.objects.update_or_create(
                    id=data["id"],  # Look for a Chapter with this id
                    defaults={
                        "name_simple": data["name_simple"],
                        "name_complex": data["name_complex"],
                        "name_arabic": data["name_arabic"],
                        "revelation_place": data["revelation_place"],
                        "revelation_order": data["revelation_order"],
                        "bismillah_pre": data["bismillah_pre"],
                        "verses_count": data["verses_count"],
                        "pages": data["pages"],
                        "translated_name": data["translated_name"]["name"],
                    }
                )
            else:
                self.stdout.write(self.style.ERROR(f"Failed to fetch chapter {chapter_id}"))

        self.stdout.write(self.style.SUCCESS("Chapters stored successfully."))
