from library.controller_interfaces.channel_controller_interface import IChannelController
from library.models import Channel


class ChannelController(IChannelController):
    def __init__(self):
        self.model = Channel

    # Get a single channel by ID
    def get_channel_by_id(self, channel_id: str):
        return self.model.objects.get(pk=channel_id)

    # Get a list of channels by their IDs
    def get_list_channels_by_ids(self, channel_ids: list[str]):
        return self.model.objects.filter(pk__in=channel_ids)

    def get_channel_by_channel_hash(self, channel_hash: str):
        return self.model.objects.get(channel_hash=channel_hash)
    
    def get_channel_by_user_id(self, user_id: str):
        return self.model.objects.filter(channel_owner=user_id).first()
    # Modify a channel by ID
    def modify_channel_by_id(self, channel_id: str, channel_info: dict):
        try:
            channel = self.get_channel_by_id(channel_id)
            if not channel:
                return None  # Or raise a custom exception

            for key, value in channel_info.items():
                if hasattr(channel, key):
                    setattr(channel, key, value)

            channel.save()
            return channel
        except Exception as e:
            raise e  # Handle or log as needed

    # Create a new channel
    def create_channel(self, channel_info: dict):
        res = self.model.objects.create(**channel_info)
        return res
