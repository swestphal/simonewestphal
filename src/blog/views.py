from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from .models import Post
from tags.models import Tag
from .forms import EmailPostForm, CommentForm
from django.db.models import Count


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data  # in cleanded_data are the passed entries
            # send mail
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'sw@simonewestphal.de', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'post/share.html', {'post': post,
                                               'form': form,
                                               'sent': sent})


class PostListView(ListView):
    # queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 1
    template_name = 'post/list.html'
    model = Post



def post_detail(request, post):
    post = get_object_or_404(Post, slug=post,
                             status='published')

    # post.comments because of related_name in comment model
    comments = post.comments.filter(active=True)
    post_tags = post.tags.all()
    # get ids of tags ->flat=True single values instead of tuples
    post_tags_ids = post.tags.values_list('id',flat=True)
    # get posts that contains these tags except the current
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # generate a calculated field, that count number of tags shared
    # and retrieve the first four posts
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','publish')[:4]
    
    new_comment = None

    if request.method == 'POST':
        # comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment object but don't save to database yet (create model instance, but not saving)
            new_comment = comment_form.save(commit=False)
            # assign current post to the comment
            new_comment.post = post
            # save comment to database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,
                  'post/detail.html',
                  {'post': post,
                   'tags': post_tags,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts':similar_posts})
