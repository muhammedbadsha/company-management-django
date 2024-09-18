from django.db import models
from companys.models import Company
# Create your models here.
class Department(models.Model):
    department = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.department