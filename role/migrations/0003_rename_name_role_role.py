# Generated by Django 5.1.1 on 2024-09-17 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0002_remove_role_company_role_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='role',
            old_name='name',
            new_name='role',
        ),
    ]
