
from django.contrib import  admin 
from django.urls import path, include
from . import views

# Creating the urls patterns for the Blog App
urlpatterns = [
    
    path('<str:slug>', views.blogpost, name='slug'),
    path('like/<str:slug>', views.like, name='like'),
    

]
