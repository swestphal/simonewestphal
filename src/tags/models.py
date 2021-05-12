from django.db import models
from django.db.models.signals import pre_save, post_save
#from django.urls import reverse
from django.shortcuts import get_object_or_404

from website.utils import unique_slug_generator
#from blog.models import Post
# Create your models here.


class TagQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class TagManager(models.Manager):
    def get_queryset(self):
        return TagQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_posts(self, tag_ids=[]):
        qs = None
        # qs = Post.objects.all()  # queryset  ->put in POST?
        # doc: Post.objects is object manager
        #qs = Post.objects.all()
        if tag_ids:
            qs = qs.filter(
                tags__in=[tag_ids])  # all active Tags
        return qs

    def get_tags_of_post(self, id):
        qs = Tag.objects.all().filter(blogarticle=id)
        print(qs)
        return qs


class Tag(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(default='-')
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    blogarticle = models.ManyToManyField(
        "blog.Post", blank=True, related_name='tags')

    def __str__(self):
        return self.title

    # missing this was the error "type object 'X' has no attribute 'objects'"
    objects = TagManager()


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)
