from django.db import models

# Create your models here.
class Role(models.Models):
    role_name: models.CharField(max_length=50)

class User(models.Model):
    user_name: models.CharField(max_length=50)
    user_email: models.CharField(max_length=100)
    role_id: models.ForeignKey(Role, on_delete=models.CASCADE)
