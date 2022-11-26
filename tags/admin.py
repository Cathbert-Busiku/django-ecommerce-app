from django.contrib import admin
from .models import Tag

# Register your models here.
# admin.site.register(Tag)
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['label']
