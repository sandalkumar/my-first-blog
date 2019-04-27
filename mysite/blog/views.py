from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import get_object_or_404

# TEMPLATES:
#   blog/base.html
#   blog/list_blogs.html
#   blog/detail_blog.html
#   blog/manage_list_blogs.html
#   blog/manage_add_blog.html
def render_base(request):
    return render(request, 'blog/base.html', {})

def post_list(request):
    # TODO: Blog list
    dictV ={}
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-pk')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_details(request, pk):
    # TODO: Blog Detail:
    #               url: /blog/<pk>
    dictV ={}
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/details_blog.html', {'post': post})


# TODO: Add blog:
#               url: /manage/addblog/
#               login required
def add_blog(request):
    return render( request, 'blog/add_blog.html',{})

# TODO:  List Blogs: Logged in user
#               url: /manage/list
#               login required
#               List all blogs in table format with buttons < Edit / Delete >

# TODO: Edit Blog:
#               url: /manage/edit/<pk>
#               login required

# TODO: Delete Blog:
#               url: /manage/delete_blog
#               AJAX Endpoint
