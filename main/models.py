from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.


class Profile(models.Model):
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=250)
    slug = models.SlugField(null=True, blank=True, unique=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = "Posts"
    

class Replies(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = "Reply"
        verbose_name_plural = "Replies"