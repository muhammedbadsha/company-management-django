from django.db import models
from companys.models import Company
# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
