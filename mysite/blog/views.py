from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.decorators import login_required

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


# TODO:  List Blogs: Logged in user
#               url: /manage/list
#               login required
#               List all blogs in table format with buttons < Edit / Delete >
def login_page(request):
    # TODO: If already logged in then redirect to /student/ or /staff/ depending upon the type of user.

    dictV = {}
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        user = auth.authenticate(username = username, password = password)
        print(username, password, user)
        if not user:
            dictV['error'] = "Invalid username and password combination."
            return render(request, 'blog/login.html', dictV)
        auth.login(request, user)
        print('loged in')
        return HttpResponseRedirect('/')
    return render(request,'blog/login.html',{})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
# TODO: Edit Blog:
#               url: /manage/edit/<pk>
#               login required

@login_required
def add_blog(request):
    if request.method=="POST":
       user = request.user
       title = request.POST.get('title')
       text = request.POST.get('text')
       cover = request.FILES.get('coveimage')
       print(cover)
       datestring = request.POST.get('Publishdate')
       datetime_object = datetime.strptime(datestring, '%m/%d/%Y %I:%M %p') 
       p = Post( author=user, title=title, text=text,published_date=datetime_object, cover=cover)
       p.save()
       print(p)
    print("Rendering")
    return render(request, 'blog/user_dashboard.html',{})
# TODO: Delete Blog:
#               url: /manage/delete_blog
#               AJAX Endpoint
@login_required
def edit_blog(request, pk):
    dictV = {}   
    post = get_object_or_404(Post, pk=pk)
    user = post.author
    if request.user == user:
        if request.method =="POST":
           post.title = request.POST.get('title')
           post.text = request.POST.get('text')
           post.cover = request.FILES.get('coveimage')
           datestring = request.POST.get('Publishdate')
           post.published_date = datetime.strptime(datestring, '%m/%d/%Y %I:%M %p') 
           post.save()
           dictV['message'] = "Blog Post Updated !!"
    else:
        return HttpResponseRedirect('/')
    dictV['post'] = post
    return render(request, 'blog/edit_blog.html', dictV)

@login_required
def delete_blog(request, pk):
    dictV = {}   
    post = get_object_or_404(Post, pk=pk)
    confirmed = request.GET.get('confirm')
    user = post.author
    if request.user == user:
        if confirmed == 'yes':
            post.delete()
            return HttpResponseRedirect('/')
        dictV['post'] = post
    else:
        return HttpResponseRedirect('/')   
    return render(request, 'blog/delete_blog.html', dictV)