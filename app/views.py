from django.shortcuts import get_object_or_404

from models import Post
from tools import view, Paginator

@view
def home(request, page = 1):
    page = int(page)

    paginator = Paginator(Post.objects.all(), 3)

    return {
        'posts': paginator.page(page),
        'page' : page,
        'pages': paginator.num_pages,

        'prev': {
            'num': page -1,
            'url': '/%d' % (page - 1)
        } if page > 1 else None,

        'next': {
            'num': page + 1,
            'url': '/%d' % (page + 1)
        } if page < paginator.num_pages else None
    }

@view
def single(request, slug):
    return { 'post': get_object_or_404(Post, slug = slug) }

@view
def archives(request):
    return { 'posts': Post.objects.all() }    