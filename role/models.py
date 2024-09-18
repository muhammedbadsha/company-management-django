from django.db import models
from departments.models import Department
# Create your models here.

class Role(models.Model):
    role = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True)
    def __str__(self) -> str:
        return self.role