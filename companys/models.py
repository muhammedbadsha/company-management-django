from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    contact_info = models.TextField()
    logo = models.ImageField(upload_to='logos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

