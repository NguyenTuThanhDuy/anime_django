from django.db import models

# Create your models here.
class Channel(models.Model):
    channel_id = models.UUIDField(name='channel_id', primary_key=True, editable=False)
    channel_name = models.CharField(name='channel_name', max_length=255, blank=False)
    profile_url = models.CharField(name='channel_profile_url', max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

class Video(models.Model):
    video_id = models.UUIDField(name='video_id', primary_key=True, editable=False)
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
