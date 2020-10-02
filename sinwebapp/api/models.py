from django.db import models
from django.contrib.auth.models import User
import datetime

# For formatting purposes.
STATUS_FIELDS = ['id', 'name', 'description']
# Used for verfying request GET query parameters and POST body parameters
SIN_FIELDS={ 1: 'id', 2: 'sin_number', 3: 'user_id', 4: 'status_id', 5: "sin_description", 6:"sin_title" }
# Dictionary for querying Status model by ID via API
STATUS_STATES = { 'submitted': 1, 'reviewed': 2, 'change': 3, 'approved': 4, 'denied': 5, 'expired': 6 }


class Status(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)

class SinData(models.Model):
    sin_number = models.CharField(max_length=1000)
    sin_title = models.CharField(max_length=1000, null=True)
    sin_description = models.TextField(null=True)
    special_item_number = models.CharField(max_length=1000, null=True)
    begin_date = models.DateField('Creation Date')
    end_date = models.DateField('End Date', null=True)
    state_and_local = models.BooleanField()
    set_aside = models.BooleanField()
    service_comm_code = models.CharField(max_length=1)
    psc_code = models.CharField(max_length=1)
    tdr_flag = models.BooleanField()
    olm_flag = models.BooleanField()
    max_order_limit = models.IntegerField()

class Sin(models.Model):
    sin_map = models.ForeignKey(SinData, on_delete=models.PROTECT, null= True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    sin_number = models.CharField(max_length=1000)
    sin_title = models.CharField(max_length=1000, null=True)
    sin_description = models.CharField(max_length=1000, null=True)

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