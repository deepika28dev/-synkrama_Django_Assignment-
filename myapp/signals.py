# myapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Post
from django.contrib.auth.models import User

@receiver(post_save, sender=Post)
def send_email_on_post_creation(sender, instance, created, **kwargs):
    if created:
        subject = 'New Post Created'
        message = f'Hello {instance.author.username}, a new post "{instance.title}" has been created.'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.author.email])
