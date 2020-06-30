# Generated by Django 2.2.10 on 2020-06-25 12:13

from django.db import migrations
from ..db_config import init_groups, init_permissions, init_users, init_group_permissions

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(init_groups),
        migrations.RunPython(init_permissions),
        migrations.RunPython(init_users)
    ]
