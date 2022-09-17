# Data base file
from pyexpat import model
from tkinter import CASCADE
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib import admin

# Creating the Database for the Post
INT_CHOICES = (
    ("Food", "Food"),
    ("Technology", "Technology"),
    ("Travel", "Travel"),
    ("Entertainment", "Entertainment"),
    ("Gaming", "Gaming"),
    ("Health & Fitness", "Health & Fitness"),
    ("Political", "Political"),
    ("Education", "Education"),
    ("Fashion", "Fashion"),
    ("General", "General"),
  
)

class Post(models.Model):
    
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category  = models.CharField(
        max_length = 50,
        choices = INT_CHOICES,
        default = 'college'
        )
    likes = models.IntegerField(default=0)
    timestamp = models.DateField(blank=True)
    image = models.ImageField(upload_to="thumbnails/")
  
    
    def __str__(self):
        return self.title

class Likes(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.CharField(max_length=50)
    post_sno = models.IntegerField()
    






