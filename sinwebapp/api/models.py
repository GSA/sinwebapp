from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    status = models.IntegerField(null=False)
    description = models.CharField(max_length=200)

class Sin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    sin_number = models.IntegerField(null=False)

class Audit_Log(models.Model):
    sin = models.ForeignKey(Sin, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField('Creation Date')
    updated_date = models.DateTimeField('Update Date')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sin = models.ForeignKey(Sin, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)