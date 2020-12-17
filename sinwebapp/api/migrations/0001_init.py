# Generated by Django 2.2.17 on 2020-12-16 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SinData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sin_number', models.CharField(max_length=1000)),
                ('sin_title', models.CharField(max_length=1000, null=True)),
                ('sin_description', models.TextField(null=True)),
                ('special_item_number', models.CharField(max_length=1000, null=True)),
                ('begin_date', models.DateField(verbose_name='Creation Date')),
                ('end_date', models.DateField(null=True, verbose_name='End Date')),
                ('state_and_local', models.BooleanField()),
                ('set_aside', models.BooleanField()),
                ('service_comm_code', models.CharField(max_length=1)),
                ('psc_code', models.CharField(max_length=1)),
                ('tdr_flag', models.BooleanField()),
                ('olm_flag', models.BooleanField()),
                ('max_order_limit', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Sin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sin_number', models.CharField(max_length=1000)),
                ('sin_title', models.CharField(max_length=1000, null=True)),
                ('sin_description', models.CharField(max_length=1000, null=True)),
                ('sin_map', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.SinData')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1000)),
                ('sin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Sin')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Audit_Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True, verbose_name='Creation Date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('sin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Sin')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
