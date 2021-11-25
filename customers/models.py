from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)

    photo = models.ImageField(null=True, upload_to='customer_photos')

    birthday = models.DateField(null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(null=True, max_length=20)

    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='creator')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='editor')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
