from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name','id','manager','skype_id']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','owner']