from django.contrib import admin
from django.contrib import admin
from .models import Upload

# Register your models here.
@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = (
        'get_uploaded_file_name',       # Display file name only
        'original_filename',
        'uploaded_at',
        'dos_count',
        'normal_count'
    )
    list_filter = ('uploaded_at',)
    search_fields = ('original_filename', 'user__username')

    def get_uploaded_file_name(self, obj):
        return obj.csv_file.name if obj.csv_file else 'No file'
    get_uploaded_file_name.short_description = 'Uploaded File'