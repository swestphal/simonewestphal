from django.db import models
from django.db.models.signals import pre_save, post_save
#from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from website.utils import unique_slug_generator
#from blog.models import Post
# Create your models here.
import blog.models

class TagQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    



class Tag(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(default='-')
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    #blogarticle = models.ManyToManyField(
     #   'self')
    post = models.ForeignKey(
        "blog.Post", blank=True, on_delete=models.DO_NOTHING ,related_name='tags_of_posts',null=True)
  
    def __str__(self):
        return self.title
    
    # missing this was the error "type object 'X' has no attribute 'objects'"
    objects = TagManager()

    def get_absolute_url(self):
        return reverse('tags:tag-detail',
                       args=[
                           self.slug])
    

def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)
