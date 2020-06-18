from django.db import models

# Create your models here.

class User(models.Model):
    user_name: models.CharField(max_length=100)
    user_email: models.CharField(max_length=200)
    user_role: models.CharField(max_length=50)
