# serializers.py
from rest_framework import serializers
from .models import Post,BlockedUser

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    author_email = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'author_username', 'author_email', 'created_at', 'updated_at']

class BlockedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedUser
        fields = ['id', 'user', 'blocked_user']
