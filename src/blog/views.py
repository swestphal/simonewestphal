from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from .models import Post
from tags.models import Tag
from .forms import EmailPostForm, CommentForm


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


class PostDetailView(DetailView):
    context_object_name = 'post'
    template_name = 'post/detail.html'


# see here
def get_object(self):
    qs = Order.objects.by_request(self.request).filter(
        order_id=self.kwargs.get('order_id'))
    if qs.count() == 1:
        return qs.first()
    raise Http404

    # end seehere


def get_object(self, *args, **kwargs):
    #     request = self.request
    #     slug = self.kwargs.get('post')
    #     return slug
    return Post.objects.get(slug=self.kwargs.get('post'))

# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 1)  # 1 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     print(page)
#     return render(request,
#                   'post/list.html',
#                   {'page': page,
#                    'posts': posts})


# outdated
def post_detail(request, post):
    post = get_object_or_404(Post, slug=post,
                             status='published')

    # post.comments because of related_name in comment model
    comments = post.comments.filter(active=True)

    tags = Tag.objects.get_tags_of_post(post.id)

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
                   'tags': tags,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})
