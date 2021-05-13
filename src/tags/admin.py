from django.contrib import admin
from .models import Tag
# Register your models here.
from blog.models import Post
from django.forms import CheckboxSelectMultiple





class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'active')
    list_filter = ('title', 'slug', 'active')
    search_fields = ('title', 'slug', 'active')
    model = Tag
    





admin.site.register(Tag,TagAdmin)
