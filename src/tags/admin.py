from django.contrib import admin
from .models import Tag
# Register your models here.


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'active')
    list_filter = ('title', 'slug', 'active')
    search_fields = ('title', 'slug', 'active')
