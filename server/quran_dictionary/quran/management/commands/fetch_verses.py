import requests
from django.core.management.base import BaseCommand
from quran.models import QuranWord, Chapter, Juz

class Command(BaseCommand):
    help = "Fetch Quran verses and store words in the database."


    def handle(self,*args,**kwargs):
        response=requests.get("https://api.quran.com/api/v4/quran/verses/indopak")
        if response.status_code==200:
            data=response.json()
            verses=data.get("verses",[])

            for verse in verses:
                verse_id=verse["id"]
                verse_key=verse["verse_key"]
                text=verse["text_indopak"]

                chapter_number = int(verse_key.split(":")[0])


                chapter=Chapter.objects.get(id=chapter_number)

                juz=Juz.objects.filter(
                    first_verse_id__lte=verse_id,
                    last_verse_id__gte=verse_id
                ).first()
                
                words = text.split()


                for word in words:

                    QuranWord.objects.get_or_create(
                            verse_id=verse_id,
                            verse_key=verse_key,
                            word=word,
                            meaning=None,
                            defaults={
                            'meaning': None, 
                            'chapter': chapter,
                            'juz': juz
                        }

                    )

                    self.stdout.write(self.style.SUCCESS("words stored successfully without meaning."))
                else:
                    self.stdout.write(self.style.ERROR("Failed to fetch data from the API."))

                



