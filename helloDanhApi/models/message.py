from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .messageplacement import MessagePlacement

class Message(models.Model):
    '''
    description: This class creates a message and its properties
    properties:
        message/text
        whther message is enabled
        message placement
        user related to
    '''

    message = models.TextField(max_length=1200)
    message_enabled = models.BooleanField(default=True)
    message_placement = models.ForeignKey(MessagePlacement, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.CASCADE)