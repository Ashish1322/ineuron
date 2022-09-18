# Importing the some libraries and functions which are required for the site
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .models import Post
from .models import Likes
from django.contrib import messages
from blog.templatetags import extras

# Function to like
def like(request,slug):
    if request.user.is_authenticated:
        # before increain like we check if its already liked by current user or not
        try:
            Likes.objects.get(user=request.user.username,post_sno = int(slug))
            return redirect("home")
        except Exception as e:

            a = Post.objects.get(sno = int(slug))
            a.likes = a.likes+1
            a.save()
            temp = Likes.objects.create(user=request.user.username,post_sno = int(slug))
            temp.save()
    return redirect("home")


# Fetching the blog with required sno as slug and sending to blogpost.html with the comments and replies
def blogpost(request,slug):
    a = Post.objects.filter(sno = slug) # Fetching the required Post
    # Handling the number of view (Please suggest Improvements)
    b = Post.objects.filter(sno = slug).first()
    # Give 5 trending posts by their likes
    trending =  Post.objects.all().order_by('-likes')

    # Sending all the variables to the blogpost.html file 
    return render(request,'blog/blogpost.html',{'post':a[0],'trending':trending[0:5],})

