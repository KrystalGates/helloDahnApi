from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class AlertPlacement(models.Model):
    '''
    description: This class creates a alertplacement and its properties
    property:
        alert placement
    '''

    color = models.CharField(max_length=50)