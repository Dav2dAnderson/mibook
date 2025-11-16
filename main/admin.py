from django.contrib import admin

from .models import Profile, Post, Replies
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'author', 'total_likes']


@admin.register(Replies)
class RepliesAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']

    

