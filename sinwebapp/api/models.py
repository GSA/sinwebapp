from django.db import models
from django.contrib.auth.models import User
import datetime

STATUS_FIELDS = ['id', 'name', 'description']
SIN_FIELDS={ 1: 'id', 2: 'sin_number', 3: 'user_id', 4: 'status_id' }
STATUS_STATES = { 'submitted': 1, 'reviewed': 2, 'change': 3, 'approved': 4, 'denied': 5, 'expired': 6 }


class Status(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

class SinData(models.Model):
    sin_number = models.CharField(max_length=1000)
    schedule_number = models.CharField(max_length=1000, null=True)
    special_item_number = models.CharField(max_length=1000, null=True)
    sin_group_title = models.CharField(max_length=1000, null=True)
    sin_description1 = models.TextField(null=True)
    sin_description2 = models.TextField(null=True)
    sin_order = models.CharField(max_length=1000, null=True)
    co_fname = models.CharField(max_length=1000, null=True)
    co_lname = models.CharField(max_length=1000, null=True)
    co_phone = models.CharField(max_length=1000, null=True)
    co_email = models.CharField(max_length=1000, null=True)

class Sin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    sin_number = models.CharField(max_length=1000)
    sin_group_title = models.CharField(max_length=1000, null=True)
    sin_description1 = models.CharField(max_length=1000, null=True)
    sinMap = models.ForeignKey(SinData, on_delete=models.SET_NULL, null= True)

class Audit_Log(models.Model):
    sin = models.ForeignKey(Sin, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('Creation Date', auto_now=True)
    updated_date = models.DateTimeField('Update Date', auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sin = models.ForeignKey(Sin, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)