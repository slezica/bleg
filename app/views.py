from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from models import Post
from forms import CommentForm
from tools import view, Paginator

@view
def home(request, page = 1):
    page = int(page)

    paginator = Paginator(Post.objects.all(), 3)

    return {
        'posts': paginator.page(page),
        'page' : page,
        'pages': paginator.num_pages,
    }

@view
def single(request, slug):
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save()
            return redirect('{0}#comment-{1}'.format(request.path, comment.id))

    else:
        form = CommentForm()

    return {
        'post': get_object_or_404(Post, slug = slug),
        'form': form
    }

@view
def archives(request):
    return { 'posts': Post.objects.all() }