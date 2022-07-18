from PyQt5.QtCore import QThread, pyqtSignal

from download.douyin_v2 import DouyinDownloader
from download.youtube import YoutubeDownloader
import os


class DownloadThread(QThread):
    #  通过类成员对象定义信号对象
    _download_signal = pyqtSignal(int)

    def __init__(self, web, home_page_url, save_path, translate_to_english):
        super(DownloadThread, self).__init__()
        self.website = web
        self.autoloader = self.__create_downloader__()
        self.target_link = home_page_url
        self.save_path = save_path
        self.translate_to_english = translate_to_english

    def __create_downloader__(self):
        web = self.website
        if web == "douyin":
            # 创建下载器
            return DouyinDownloader()
        elif web == 'youtube':
            return YoutubeDownloader()
        else:
            return None

    def __del__(self):
        self.wait()

    def run(self):
        '''
        创建下载对象
        :return:
        '''
        if self.target_link is None:
            return

        # 解析
        self._download_signal.emit(-1)
        nickname, parsed_urls_names = self.autoloader.parseUrl(self.target_link, self.translate_to_english)
        self._download_signal.emit(-2)

        video_count = len(parsed_urls_names)
        # 保存路径
        nickname_dir = os.path.join(self.save_path, nickname)
        if not os.path.exists(nickname_dir):
            os.makedirs(nickname_dir)
        # 下载
        for i in range(video_count):
            item = parsed_urls_names[i]
            video_url = item[0]
            video_name = item[1]
            self.autoloader.download(video_url, video_name, nickname_dir)
            self._download_signal.emit(int((i+1) / video_count * 100))