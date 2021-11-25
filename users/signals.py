from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def post_create_user(sender, **kwargs):
    if kwargs.get('created'):
        # Create tocket after create a new user
        Token.objects.create(user=kwargs.get('instance'))
