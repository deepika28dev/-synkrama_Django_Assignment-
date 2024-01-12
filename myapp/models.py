# models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class BlockedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocking_user')
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_user')


