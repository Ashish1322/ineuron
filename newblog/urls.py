# Importing some libraries
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Creating and hanling the urls of Main Project
urlpatterns = [
    path('admin/', admin.site.urls), # the admin of the Project
    path('', include('home.urls')), # Initially Control goes to the urls.py of Home app
    path('blog/',include('blog.urls')), # If urls contains blog then control goes to the urls.py of blog app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
