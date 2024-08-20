from django.db import models

class Chapter(models.Model):
    id = models.IntegerField(primary_key=True)
    name_simple = models.CharField(max_length=100)
    name_complex = models.CharField(max_length=100,unique=True)
    name_arabic = models.CharField(max_length=100)
    revelation_place = models.CharField(max_length=50)
    revelation_order = models.IntegerField()
    bismillah_pre = models.BooleanField()
    verses_count = models.IntegerField()
    pages = models.JSONField()
    translated_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name_simple

class Juz(models.Model):
    id = models.IntegerField(primary_key=True)
    juz_number = models.PositiveIntegerField()
    first_verse_id = models.IntegerField()
    last_verse_id = models.IntegerField()
    verses_count = models.IntegerField()
    verse_mapping = models.JSONField()

    def __str__(self):
        return f"Juz {self.juz_number}"

class QuranWord(models.Model):
    verse_id = models.IntegerField()
    verse_key = models.CharField(max_length=10)
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=255, blank=True, null=True)
    transcription=models.CharField(max_length=255,blank=True,null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    juz = models.ForeignKey(Juz, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.word} ({self.meaning or 'meaning not entered'})"
