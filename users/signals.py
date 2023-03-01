from django.contrib.auth.models import User  # Where is the user created when we register? -In the User Table
from django.db.models.signals import post_save  # Send signals immediately after the user is created
from django.dispatch import receiver  # catch signals

from rest_framework.authtoken.models import Token  # The table we will create tokens after capturing the signals

from .models import Profile

@receiver(post_save, sender = User)  # After the user is created, the following event will occur.
def crate_Token(sender, instance = None, created = False, **kwargs):  # instance represents User here. created is False by default, returns True when created.
    if created:
        Token.objects.create(user = instance)
    

#? Thanks to Signals, we generated tokens when the user registered, so the user did not have to login again after registering.
#! Not: Normally signals are defined in models.py, since we define external, we need to make some changes in apps.py page.



#! We write signals to automatically create profile page when User is Register
@receiver(post_save, sender = User)
def create_profile(sender, instance = None, created = False, **kwargs):
    if created:
        Profile.objects.create(user = instance)
