import random
import re

from rest_framework import serializers

from library.models import Channel, Video
from library.controllers.channel_controller import ChannelController

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('video_id', 'title', 'channel', 'views', 'posted_at', 'duration', 'thumbnail_url', 'video_url')
        read_only_fields = ('video_id', 'posted_at', 'duration', 'channel')

    def create(self, validated_data):
        user_video_data = {}

        video_record = Video.objects.create(**user_video_data)

        return video_record

    def update(self, instance, validated_data):
        # Update each field in the instance that is provided in validated_data
        for field, value in validated_data.items():
            setattr(instance, field, value)
        
        # Save the updated instance to the database
        instance.save()
        return instance

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('channel_id', 'channel_name', 'profile_url')
        read_only_fields = ('channel_id', 'channel_hash', 'channel_owner', 'created_at')

    def create(self, validated_data):
        pattern = r"\s+"
        channel_hash = re.sub(pattern, "", validated_data['channel_name'])
        channel_hash = f"@{channel_hash}{random.randint(0, 1000)}"
        while True:
            is_exist = ChannelController().get_channel_by_channel_hash(channel_hash)
            if not is_exist:
                break
            channel_hash = f"@{validated_data['channel_name']}{random.randint(0, 1000)}"

        validated_data['channel_hash'] = channel_hash
        channel_record = ChannelController().create_channel(validated_data)

        return channel_record

    def update(self, instance, validated_data):
        # Update each field in the instance that is provided in validated_data
        for field, value in validated_data.items():
            setattr(instance, field, value)
        
        # Save the updated instance to the database
        instance.save()
        return instance

class ChannelIDsSerializer(serializers.Serializer):
    channel_ids = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        help_text="A list of channel IDs as strings."
    )