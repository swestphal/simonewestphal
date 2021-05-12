from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
#from .models import Post
from tags.models import Tag


class TagDetailView(ListView):
    try:
        tag_id = get_object_or_404(Tag, slug='django')
        queryset = Tag.objects.get_posts(tag_id)
        tag_found = True
    except:
        queryset = Tag.objects.get_posts()
        tag_found = False

    context_object_name = 'tags'
    paginate_by = 1
    template_name = 'tags/list.html'

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['tag_found'] = self.tag_found
        return context
