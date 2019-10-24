from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):

    address = models.CharField(max_length=250)
    phone_number = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
