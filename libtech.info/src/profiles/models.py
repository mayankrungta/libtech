from django.conf import settings
from django.db import models
from allauth.account.signals import user_logged_in, user_signed_up

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
class profile(models.Model):
    name = models.CharField(max_length=1200)
    description = models.TextField(default='Description default')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)

    def __str__(self):
        return self.name

class userStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if self.stripe_id:
            return self.stripe_id
        else:
            return self.user.username

def stripe_callback(sender, request, user, **kwargs):
    user_stripe_account, created = userStripe.objects.get_or_create(user=user)
    if created:
        print('Created For[%s]' % user.username)

    if not user_stripe_account.stripe_id or user_stripe_account.stripe_id == '':
        user_stripe_account.stripe_id = stripe.Customer.create(email=user.email)['id']
        user_stripe_account.save()

def profile_callback(sender, request, user, **kwargs):
    user_profile, created = profile.objects.get_or_create(user=user)
    if created:
        print('Profile For[%s]' % user.username)
        user_profile.name = user.username
        user_profile.save()

user_signed_up.connect(profile_callback)
user_signed_up.connect(stripe_callback)
user_logged_in.connect(stripe_callback)

