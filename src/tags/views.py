from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
#from .models import Post
from tags.models import Tag
from blog.models import Post

class TagListView(ListView):
    context_object_name = 'tags'
    paginate_by = 10
    template_name = 'tags/list.html'
    model=Tag
    
    
class TagPostListView(ListView):
    context_object_name = 'tags'
    paginate_by = 10
    template_name = 'tags/list.html'
    model=Tag
    def get_context_data(self, **kwargs):
            context = super(TagPostListView, self).get_context_data(**kwargs)
            #context['tag_found'] = self.tag_found
            return context

    def get_queryset(self, *args, **kwargs):
        #posts =  Tag.objects.get_posts(slug=self.kwargs.get('slug'))   
        tag=Tag.objects.get(slug=self.kwargs.get('slug'))
        posts_of_tag = tag.posts.all()
        return posts_of_tag