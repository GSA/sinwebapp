# Generated by Django 2.2.10 on 2020-07-31 12:07

from django.db import migrations
from ..db_init import init_default_users


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_group_permissions'),
    ]

    operations = [
        migrations.RunPython(init_default_users)
    ]
