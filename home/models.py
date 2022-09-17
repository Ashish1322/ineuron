# Database file for the Home app
from django.db import models


# Creating the Database for the Contact me Form
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    message = models.CharField(max_length=5000)
    email = models.EmailField(max_length=50)
    def __str__(self):
        return self.name
    





