from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import QuranWord, Juz, Chapter

# Define resources for each model
class QuranWordResource(resources.ModelResource):
    class Meta:
        model = QuranWord
        import_id_fields = ['id']
      

class JuzResource(resources.ModelResource):
    class Meta:
        model = Juz
        import_id_fields = ['id']
        

class ChapterResource(resources.ModelResource):
    class Meta:
        model = Chapter
        import_id_fields = ['id']
        

# Register the models with ImportExportModelAdmin
@admin.register(QuranWord)
class QuranWordAdmin(ImportExportModelAdmin):
    resource_class = QuranWordResource

@admin.register(Juz)
class JuzAdmin(ImportExportModelAdmin):
    resource_class = JuzResource

@admin.register(Chapter)
class ChapterAdmin(ImportExportModelAdmin):
    resource_class = ChapterResource
