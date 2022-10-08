from abc import ABC
from argparse import ArgumentParser
import os
from contextlib import closing
from urllib.parse import parse_qsl, urlparse
import requests

from download.AutoDownLoader import AutoDownLoader


class TiktokDownloader(AutoDownLoader, ABC):
    def __init__(self):
        self.headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'video',
        'Referer': 'https://www.tiktok.com/',
        'Accept-Language': 'en-US,en;q=0.9,bs;q=0.8,sr;q=0.7,hr;q=0.6',
        'sec-gpc': '1',
        'Range': 'bytes=0-',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'upgrade-insecure-requests': '1',
        }

    def parseUrl(self, home_page_url):
        response = requests.get(home_page_url, headers=self.headers)
        urls = response.text.split('"playAddr":"')[1].split('"')[0].replace(r'\u0026', '&')
        return urls

    def download(self, video_url, video_name, save_path):
        '''
        下载单个视频
        :param video_name:
        :param video_url:
        :param save_path:
        :param translate_to_english:
        :return:
        '''

        with closing(requests.get(video_url, headers=self.headers, stream=True)) as response:
            chunk_size = 102400
            video_name = video_name[:min(len(video_name), 100)]
            if response.status_code == 200:
                i = 0
                while os.path.exists(save_path + os.sep + video_name + '.mp4'):
                    video_name = video_name.replace("_" + str(i), "")
                    i += 1
                    video_name += ("_" + str(i))

                file_path = save_path + os.sep + video_name + '.mp4'
                with open(file_path, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)


if __name__ == "__main__":
    url = 'https://www.tiktok.com/@andcarli/video/7136971648669895941?is_from_webapp=1&sender_device=pc&web_id=7136917778469045762'
    down = TiktokDownloader()
    xx = down.parseUrl(url)
    down.download(xx, "aa", "E:/")
    