# Generated by Django 2.2.10 on 2020-06-30 16:51

from django.db import migrations
from ..db_config import init_group_permissions

class Migration(migrations.Migration):

    dependencies = [
        ('authentication','0001_initial'),
    ]

    operations = [
        migrations.RunPython(init_group_permissions)
    ]
