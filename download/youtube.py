import os
from pytube import YouTube
from abc import ABC
import re
import urllib.request
import urllib.error

from download.AutoDownLoader import AutoDownLoader


class YoutubeDownloader(AutoDownLoader, ABC):
    def __init__(self):
        pass

    def parseUrl(self, home_page_url):
        parsed_urls_names = []

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
            video_name = yt.title

            # 判断重名、长度等
            video_name = video_name[:min(len(video_name), 50)]
            i = 0
            while os.path.exists(save_path + os.sep + video_name + '.mp4'):
                video_name = video_name.replace("_" + str(i), "")
                i += 1
                video_name += ("_" + str(i))

            video.download(save_path, video_name)
        except OSError:
            return