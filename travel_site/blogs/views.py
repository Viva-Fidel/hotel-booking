from django.shortcuts import render, get_object_or_404
from .models import Blogs

# Create your views here.

def blog_detail(request, slug):
    blog = get_object_or_404(Blogs, slug=slug)
    context = {'blog': blog}
    return render(request, 'blog/blog_detail.html', context)
