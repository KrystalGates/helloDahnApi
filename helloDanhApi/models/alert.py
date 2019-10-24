from django.db import models
from .customuser import CustomUser
from .alertplacement import AlertPlacement

class Alert(models.Model):
    '''
    description: This class creates a alert and its properties
    properties:
        alert/text
        whther alert is enabled
        alert placement
        user related to
    '''

    alert = models.TextField(max_length=1200)
    alert_enabled = models.BooleanField(default=True)
    alert_placement = models.ForeignKey(AlertPlacement, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)