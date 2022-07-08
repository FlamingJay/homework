import os
import re
import time

import requests
from abc import ABC
from contextlib import closing

from AutoDownLoader import AutoDownLoader
import Translator


class DouyinDownloader(AutoDownLoader, ABC):
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        }

    def parseUrl(self, home_page_url, translate_to_english):
        '''
        解析主页链接，返回所有的视频链接列表
        :param home_page_url:
        :return:
        '''

        parsed_urls_names = []

        requests.packages.urllib3.disable_warnings()
        session = requests.session()
        res = session.get(url=home_page_url, headers=self.headers, verify=False)
        sec_uid = re.findall(r'sec_uid=(\w+-\w+-\w+|\w+-\w+|\w+)', res.url)
        # 获取视频数量总数  用户名
        sum_url = 'https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid={0}'.format(sec_uid[0])
        se = session.get(sum_url)
        sm_count = re.findall('"aweme_count":(\w+)', se.text)
        # 用户名
        nickname = re.findall('"nickname":"(.*?)"', se.text)
        # Translator配置
        word_dict = Translator.load_word_dict()

        # 页面
        max_cursor = 0
        index = 0
        while True:
            while True:
                if max_cursor == 0:
                    sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=21&max_cursor=0&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(
                        sec_uid[0])
                else:
                    sec_id_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=21&max_cursor={1}&aid=1128&_signature=dF8skQAAK0iTKNSXi9av.XRfLI&dytk=".format(
                        sec_uid[0], max_cursor)
                sec_respone = session.get(url=sec_id_url, headers=self.headers, verify=False)
                comment = sec_respone.json()
                if len(comment['aweme_list']) == 0:
                    continue
                else:
                    break
            # 下一页下标
            max_cursor = comment['max_cursor']
            for s in comment['aweme_list']:
                index += 1
                # 无水印视频链接地址
                video_url = s['video']['play_addr_lowbr']['url_list'][0]
                # 视频名称
                video_name = re.sub(r'[\/:*?"<>|\n]', '', s['desc'])
                if translate_to_english:
                    try:
                        time.sleep(1)
                        video_name = Translator.word_replace(video_name, word_dict)
                        video_name = Translator.baiduAPI_translate(query_str=video_name, from_lang='zh',
                                                                                  to_lang='en')

                    except:
                        video_name = video_name
                parsed_urls_names.append([video_url, video_name])

            if int(index) >= int(sm_count[0]):
                break

        return nickname[0], parsed_urls_names

    def download(self, video_url, video_name, save_path):
        '''
        下载单个视频
        :param video_name:
        :param video_url:
        :param save_path:
        :param translate_to_english:
        :return:
        '''

        size = 0
        with closing(requests.get(video_url, headers=self.headers, stream=True)) as response:
            chunk_size = 1024
            if response.status_code == 200:
                while os.path.exists(video_name + '.mp4'):
                    video_name += "_"

                video_name = video_name + '.mp4'
                file_path = save_path + os.sep + video_name
                with open(file_path, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()