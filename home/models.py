from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    mail_id = models.EmailField(unique=True)
    password = models.CharField(max_length=501)
    skype_id = models.CharField(max_length=100,unique=True)
    project = models.CharField(max_length=100)
    posts = models.JSONField(null=True)
    manager = models.ForeignKey('User',null=True,on_delete=models.CASCADE)
    skills = models.JSONField(null = True)
    links = models.JSONField(null = True)

class Post(models.Model):
    content = models.TextField()
    owner = models.ForeignKey("User",on_delete=models.CASCADE)
    date_created = models.DateField()
    upvotes = models.IntegerField(default=0)
    comments = models.JSONField(null=True)
    tags = models.JSONField(null=True)

class comment(models.Model):
    owner = models.ForeignKey("User",on_delete=models.CASCADE)
    post = models.ForeignKey("Post",on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateField()
    upvotes = models.IntegerField(default=0)