from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'Follow'
        verbose_name_plural = "Follows"

# !!!
# user.followers.all()      Menga kimlar follow qilyapti
# user.following.all()      Men kimlarga follow qilganman