from abc import abstractmethod, ABCMeta

class AutoEditor(metaclass=ABCMeta):
    @abstractmethod
    def videos_edit(self, video_list):
        pass

    @abstractmethod
    def prepare_videos(self, video_path):
        pass