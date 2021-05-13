from django.urls import path
from . import views

app_name = 'tags'

urlpatterns = [
    # post views
    path('', views.TagListView.as_view(), name='tag-list'),
    path('<slug:slug>/',
         views.TagPostListView.as_view(), name='tag-detail'),
    
]
