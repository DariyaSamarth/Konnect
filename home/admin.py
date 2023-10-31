from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name','id','manager','posts']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','owner','comments','likes']


@admin.register(comment)
class commentAdmin(admin.ModelAdmin):
    list_display = ['id','owner','post','content','likes']