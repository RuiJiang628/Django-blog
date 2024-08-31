import re
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from markdown.extensions.toc import TocExtension
from .models import Post, Category, Tag
import markdown
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    md = markdown.Markdown(extensions=[
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',
                                TocExtension(),
                          ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'post': post})

def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list': post_list})

def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t)
    return render(request, 'blog/index.html', context={'post_list': post_list})

def author(request, pk):
    auth = get_object_or_404(User, pk=pk)
    post_list = Post.objects.filter(author=auth)
    return render(request, 'blog/index.html', context={'post_list': post_list})