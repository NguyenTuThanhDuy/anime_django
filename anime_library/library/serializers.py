from rest_framework import serializers

from library.models import Channel, Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'title', 'channel', 'views', 'posted_at', 'duration', 'thumbnail_url', 'video_url')
        read_only_fields = ('id', 'posted_at', 'duration')

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'channel_name', 'profile_url')
        read_only_fields = ('id', 'channel_name', 'created_at')