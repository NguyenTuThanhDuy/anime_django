from abc import ABC, abstractmethod

class IChannelController(ABC):
    @abstractmethod
    def get_channel_by_id(self, channel_id: str):
        raise NotImplementedError()

    @abstractmethod
    def get_list_channels_by_ids(self, channel_ids: list[str]):
        raise NotImplementedError()

    @abstractmethod
    def modify_channel_by_id(self, channel_id: str, channel_info: dict):
        raise NotImplementedError()

    @abstractmethod
    def create_channel(self, channel_info: dict):
        raise NotImplementedError()
