from abc import ABC, abstractmethod

class IVideoController(ABC):
    @abstractmethod
    def get_video_by_id(self, video_id: str):
        raise NotImplementedError()

    @abstractmethod
    def get_list_videos_by_ids(self, video_ids: list[str]):
        raise NotImplementedError()

    @abstractmethod
    def modify_video_by_id(self, video_id: str, video_info: dict):
        raise NotImplementedError()

    @abstractmethod
    def create_video(self, video_info: dict):
        raise NotImplementedError()
