import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Channel(models.Model):
    channel_id = models.UUIDField(
        name='channel_id', 
        primary_key=True, 
        editable=False, 
        default=uuid.uuid4
    )
    channel_name = models.CharField(
        name='channel_name', 
        max_length=255, 
        blank=False
    )
    channel_hash = models.CharField(
        name='channel_hash', 
        max_length=64, 
        unique=True, 
        db_index=True, 
        null=True
    )
    channel_owner = models.OneToOneField(
        to=User,  # Use the default User model or replace with your custom User model
        name='channel_owner',
        on_delete=models.CASCADE, 
        related_name="owned_channel",
        null=True,
    )
    profile_url = models.URLField(
        name='profile_url', 
        max_length=500, 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.channel_name


class Video(models.Model):
    video_id = models.UUIDField(name='video_id', primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(name='video_title', max_length=255, blank=False)
    channel = models.ForeignKey(
        Channel, related_name='videos', on_delete=models.CASCADE, db_index=True
    )
    views = models.BigIntegerField(default=0)
    posted_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    duration = models.BigIntegerField(),
    thumbnail_url = models.CharField(name='video_thumbnail_url', max_length=500)
    video_url = models.CharField(name='video_url', max_length=500)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
