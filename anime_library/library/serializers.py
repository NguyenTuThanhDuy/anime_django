from rest_framework import serializers

from library.models import Channel, Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'title', 'channel', 'views', 'posted_at', 'duration', 'thumbnail_url', 'video_url')
        read_only_fields = ('id', 'posted_at', 'duration', 'channel')

    def create(self, validated_data):
        user_video_data = {}

        video_record = Video.objects.create(**user_video_data)

        return video_record

    def update(self, instance, validated_data):
        pass

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'channel_name', 'profile_url')
        read_only_fields = ('id', 'channel_name', 'created_at')

    def create(self, validated_data):
        user_channel_data = {}

        channel_record = Channel.objects.create(**user_channel_data)

        return channel_record

    def update(self, instance, validated_data):
        pass