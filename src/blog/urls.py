from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from .feeds import LatestPostsFeed

sitemaps={'posts':PostSitemap}
app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.PostListView.as_view(), name='post-list'),
    path('feed/',LatestPostsFeed(),name='post-feed'),
    path('search/',views.post_search,name='post-search'),
    path('<slug:post>/',
         views.post_detail, name='post-detail'),
    path('<int:post_id>/share/', views.post_share, name='post-share'),
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    
]
