from django.db import models
from .customuser import CustomUser


class Contact(models.Model):
    '''
    description: This class creates a contact and its properties
    properties:
        first name
        last name
        phone number
        email
        address
        user related to
    '''

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contacts')