# Importing some libraries
from django.contrib import  admin
from django.urls import path, include
from . import views

# Creating and handling all the urls in the home app
urlpatterns = [
    path('', views.bloghome, name='home'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search_result, name='search'),
    path('signup/', views.handleSignUp, name='signup'),
    path('login/', views.handleLogin, name='login'),
    path('logout/', views.handleLogout, name='logout'),
    path('populars/', views.populars, name='populars'),
    path("activate/<uidb64>/<token>",views.get, name="activate"),
    path("category/<str:slug>",views.category, name="category"),
]
