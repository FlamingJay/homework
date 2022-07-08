import os
from pytube import YouTube
from abc import ABC
import re
import time
import urllib.request
import urllib.error

from AutoDownLoader import AutoDownLoader
import Translator


class YoutubeDownloader(AutoDownLoader, ABC):
    def __init__(self):
        pass

    def parseUrl(self, home_page_url, translate_to_english):
        parsed_urls_names = []
        self.translate_to_english = translate_to_english

        # 先对home_page_url解析
        try:
            yTUBE = urllib.request.urlopen(home_page_url).read()
            yTUBE = str(yTUBE, "utf-8")
        except:
            return

        namePatt = re.compile(r'"channelId":.*?"title":"(.*?)"')
        longVideoPatt = re.compile(r'"url":"/watch\?v=(.*?)"')
        shortVideoPatt = re.compile(r'"url":"/shorts/(.*?)"')

        long_res = longVideoPatt.findall(yTUBE)
        short_res = shortVideoPatt.findall(yTUBE)
        name_res = namePatt.findall(yTUBE)
        nickname = name_res[0]

        for item in long_res:
            parsed_urls_names.append(["https://www.youtube.com/watch?v=" + item, ""])
        for item in short_res:
            parsed_urls_names.append(["https://www.youtube.com/shorts/" + item, ""])

        return nickname, parsed_urls_names

    def download(self, video_url, video_name, save_path):
        try:
            yt = YouTube(video_url)
        except Exception as e:
            return
        try:
            video = yt.streams.filter(progressive=True, file_extension="mp4").first()
        except Exception:
            video = sorted(yt.filter("mp4"), key=lambda video: int(video.resolution[:-1]), reverse=True)[0]

        try:
            out_file = video.download(save_path)
            if self.translate_to_english:
                word_dict = Translator.load_word_dict()
                title = yt.title
                name = Translator.word_replace(title, word_dict)
                new_name = Translator.baiduAPI_translate(query_str=name, from_lang='zh',
                                                         to_lang='en')

                os.rename(out_file, save_path + os.sep + str(new_name) + ".mp4")
        except OSError:
            return