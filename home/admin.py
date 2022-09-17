from django.contrib import admin
from . models import Contact

# Registring the contact model with admin
admin.site.register(Contact)