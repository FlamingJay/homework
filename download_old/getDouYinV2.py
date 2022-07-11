#!/usr/bin/env python
# encoding: utf-8

'''
自动爬虫
'''
import os
import re
import requests
from abc import ABC
from contextlib import closing

from AutoDownLoader import AutoDownLoader
from tklog import tklog


class getDouYin(AutoDownLoader, ABC):
    def __init__(self):
        '''
        Initial the custom file by some url
        '''
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        }

    def download(self, home_page_url, save_path, logger: tklog):
        requests.packages.urllib3.disable_warnings()
        session = requests.session()
        res = session.get(url=home_page_url, headers=self.headers, verify=False)
        sec_uid = re.findall(r'sec_uid=(\w+-\w+-\w+|\w+-\w+|\w+)', res.url)
        # 获取视频数量总数  用户名
        sum_url = 'https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={0}'.format(sec_uid[0])
        se = session.get(sum_url)

        # 视频数量
        sm_count = re.findall('"aweme_count":(\w+)', se.text)
        # 用户名
        nickname = re.findall('"nickname":"(.*?)"', se.text)
        nickname_dir = os.path.join(save_path, nickname[0])
        if not os.path.exists(nickname_dir):
            os.makedirs(nickname_dir)
        logger.log("当前用户：%s，共计%s个视频\n\n" % ((nickname[0], sm_count[0])))
        logger.update()
        # 页面
        max_cursor = 0
        id = 0
        while True:
            while True:
                if (max_cursor == 0):
                    sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=21&max_cursor=0&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(
                        sec_uid[0])
                else:
                    sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=21&max_cursor={1}&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(
                        sec_uid[0], max_cursor)
                sec_respone = session.get(url=sec_id_url, headers=self.headers, verify=False)
                comment = sec_respone.json()
                if (len(comment['aweme_list']) == 0):
                    continue
                else:
                    break
            # 下一页下标
            max_cursor = comment['max_cursor']
            for s in comment['aweme_list']:
                id += 1
                # 视频名称
                text = re.sub(r'[\/:*?"<>|\n]', '', s['desc'])
                # 点赞数
                dianzan = s['statistics']["digg_count"]
                # 评论数
                pinglun = s['statistics']["comment_count"]
                # 分享数
                fenxiang = s['statistics']["share_count"]
                # 无水印视频链接地址
                video_url = s['video']['play_addr_lowbr']['url_list'][0]
                text = re.sub("(\#\w+)|(\@\w+)", '', text)
                logger.log("-- 总共有{}个，这是第{}个视频，".format(str(sm_count), str(id)) + "视频名称为：{0},点赞数为:{1},评论数为:{2},分享数量为:{3}\n"
                           .format(text, str(dianzan), str(pinglun), str(fenxiang)))
                logger.update()

                text = text.replace(" |\t|\n", "")

                try:
                    video_path = os.path.join(nickname_dir, text)
                    if os.path.isfile(video_path):
                        logger.log('---视频已存在...\r')
                        logger.update()
                    else:
                        self.__video_downloader(video_url, video_path, logger)
                except Exception as e:
                    continue

            if (int(id) >= int(sm_count[0])):
                break

        return True, nickname_dir

    def __video_downloader(self, video_url, video_name, logger: tklog):
        '''
        Download the video
        :param video_url: the url of video
        :param video_name: the name of video
        :param watermark_flag: the flag of video
        :return: None
        '''
        size = 0
        # video_url = self.__get_download_url(video_url, watermark_flag=watermark_flag)
        with closing(requests.get(video_url, headers=self.headers, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:

                with open(video_name + '.mp4', 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()

    def __get_download_url(self, video_url, watermark_flag):
        '''
        Whether to download watermarked videos
        :param video_url: the url of video
        :param watermark_flag: the type of video
        :return: the url of o
        '''
        if watermark_flag == True:
            download_url = video_url.replace('api.amemv.com', 'aweme.snssdk.com')
        else:
            download_url = video_url.replace('aweme.snssdk.com', 'api.amemv.com')

        return download_url


if __name__ == '__main__':
    # https://v.douyin.com/JPrEHjx/
    do = getDouYin()
    do.download("https://v.douyin.com/FAE8CeD/", r"E:\shortVideo\getDouYin\Download")