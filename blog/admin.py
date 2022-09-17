# File for handling all the actions of the blog app
from django.contrib import admin
from . models import Post, Likes
# Register your models here.

admin.site.register(Likes)
# Registring the Post model with adding the tiny Mce as the post editor
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyinject.js',)

