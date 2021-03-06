# Generated by Django 2.2.10 on 2020-07-31 12:07

from django.db import migrations
from ..db_init import init_groups, init_permissions, init_group_permissions, init_default_users


class Migration(migrations.Migration):

    dependencies = [
        ('auth','0011_update_proxy_permissions')
    ]

    operations = [
        migrations.RunPython(init_groups),
        migrations.RunPython(init_permissions),
        migrations.RunPython(init_group_permissions),
        migrations.RunPython(init_default_users)
    ]
