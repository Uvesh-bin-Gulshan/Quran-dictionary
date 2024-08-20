import requests
from django.core.management.base import BaseCommand
from quran.models import QuranWord, Chapter, Juz
import logging

# Set up logging configuration
logging.basicConfig(filename='failed_data.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = "Fetch Quran verses and store words in the database."

    def handle(self, *args, **kwargs):
        response = requests.get("https://api.quran.com/api/v4/quran/verses/indopak")
        if response.status_code == 200:
            data = response.json()
            verses = data.get("verses", [])

            for verse in verses:
                verse_id = verse["id"]
                verse_key = verse["verse_key"]
                text = verse["text_indopak"]

                chapter_number = int(verse_key.split(":")[0])

                try:
                    chapter = Chapter.objects.get(id=chapter_number)
                except Chapter.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Chapter with id {chapter_number} does not exist."))
                    logging.error(f"Chapter with id {chapter_number} does not exist for verse ID {verse_id}.")
                    continue

                juz = Juz.objects.filter(
                    first_verse_id__lte=verse_id,
                    last_verse_id__gte=verse_id
                ).first()

                if juz is None:
                    self.stdout.write(self.style.ERROR(f"Juz for verse ID {verse_id} not found."))
                    logging.error(f"Juz for verse ID {verse_id} not found. Verse key: {verse_key}.")
                    continue

                words = text.split()

                for word in words:
                    try:
                        QuranWord.objects.get_or_create(
                            verse_id=verse_id,
                            verse_key=verse_key,
                            word=word,
                            defaults={
                                'meaning': None,
                                'chapter': chapter,
                                'juz': juz
                            }
                        )
                        self.stdout.write(self.style.SUCCESS(f"Word '{word}' stored successfully."))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Failed to store word '{word}': {str(e)}"))
                        logging.error(f"Failed to store word '{word}' for verse ID {verse_id}. Error: {str(e)}")
        else:
            self.stdout.write(self.style.ERROR("Failed to fetch data from the API."))
            logging.error("Failed to fetch data from the API. Status code: {}".format(response.status_code))
