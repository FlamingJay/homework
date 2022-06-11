#!/usr/bin/env python
# encoding: utf-8

'''
自动爬虫
'''
import os
from pytube import YouTube
from abc import ABC
import re
import time
import urllib.request
import urllib.error

from AutoDownLoader import AutoDownLoader
from tklog import tklog


class getYoutube(AutoDownLoader, ABC):
    def __init__(self):
        pass

    def download(self, home_page_url: str, save_path: str, logger: tklog):
        # 先对home_page_url解析
        try:
            yTUBE = urllib.request.urlopen(home_page_url).read()
            yTUBE = str(yTUBE)
        except:
            logger.log("视频下载get失败")
            logger.update()
            return

        longVideoPatt = re.compile(r'"url":"/watch\?v=(.*?)"')
        shortVideoPatt = re.compile(r'"url":"/shorts/(.*?)"')

        longVideosPathList = longVideoPatt.findall(yTUBE)
        shortVideoPathList = shortVideoPatt.findall(yTUBE)

        for item in longVideosPathList:
            self.__downloadSingleVideo(save_path, "https://www.youtube.com/watch?v=" + item, logger)

        for item in shortVideoPathList:
            self.__downloadSingleVideo(save_path, "https://www.youtube.com/shorts/" + item, logger)

        logger.log("下载完所有的视频了！")
        logger.update()

    def __downloadSingleVideo(self, save_path, vid_url, logger):
        try:
            yt = YouTube(vid_url)
        except Exception as e:
            logger.log("这个视频下不下来啊... " + vid_url)
            logger.update()
            return
        try:
            video = yt.streams.filter(progressive=True, file_extension="mp4").first()
        except Exception:
            video = sorted(yt.filter("mp4"), key=lambda video: int(video.resolution[:-1]), reverse=True)[0]
            logger.log("downloading " + yt.title + " Video and Audio...")
            logger.update()

        try:
            ts = time.time()
            out_file = video.download(save_path)
            os.rename(out_file, save_path + r"\\" + str(ts) + ".mp4")
            logger.log("下载完成! -- " + yt.title)
            logger.update()
        except OSError:
            logger.log("这视频已经下载过了.... " + yt.title)
            logger.update()