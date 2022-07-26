from abc import abstractmethod, ABCMeta

class AutoDownLoader(metaclass=ABCMeta):
    @abstractmethod
    def parseUrl(self, home_page_url):
        pass

    @abstractmethod
    def download(self, video_url, video_name, save_path):
        pass