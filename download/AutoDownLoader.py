from abc import abstractmethod, ABCMeta

class AutoDownLoader(metaclass=ABCMeta):
    @abstractmethod
    def download(self, home_page_url, save_path, logger):
        pass