from django.db import models
from django.core.validators import RegexValidator
# Create your models here.


class Company(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    phone_number = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Phone number must be entered in the format '+123456789'. Up to 15 digits allowed.",
            ),
        ],
    )
    email = models.EmailField(null=True)
    logo = models.ImageField(upload_to="logos/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.company_name