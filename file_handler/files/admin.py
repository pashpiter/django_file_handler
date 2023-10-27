from django.contrib import admin

from .models import File


class AdminFile(admin.ModelAdmin):
    list_display = ('pk', 'file', 'uploaded_at', 'processed',)
    list_filter = ('uploaded_at', 'processed')


admin.site.register(File, AdminFile)
