from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'mail_id',
            'skype_id',
            'project',
            'manager',
            'password',
            'posts',
            'skills',
            'links'
            ]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'owner',
            'date_created',
            'upvotes',
            'downvotes',
            'comments',
            'tags' 
            ]
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comment
        fields = [
            'id',
            'content',
            'owner',
            'date_created',
            'upvotes',
            'downvotes',
            'post'
            ]