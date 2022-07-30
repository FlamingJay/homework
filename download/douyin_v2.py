import os
import re
import json
import time

import requests
from abc import ABC
from contextlib import closing
from urllib import parse

from download.AutoDownLoader import AutoDownLoader


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

    def parseUrl(self, home_page_url):
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
        # 用户名
        nicknames = re.findall('"nickname":"(.*?)"', se.text)

        # 标题正则修改
        rstr = r"[\/\\\:;\*#￥%$!@^……&()\?\"\<\>\|\n\t]"

        try:
            url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={0}&count=21&max_cursor=0&aid=1128&_signature=R6Ub1QAAJ-gQklOOeJfpTEelG8&dytk=".format(
                sec_uid[0])
            r = requests.get(url=url, headers=self.headers, stream=True)

            # todo：返回码判断
            data_json = json.loads(r.text)
            has_more = data_json['has_more']
            max_cursor = data_json['max_cursor']
            for i in range(len(data_json['aweme_list'])):
                video_url_json = data_json['aweme_list'][i]['video']
                target_key = ""
                if 'play_addr_lowbr' in video_url_json.keys():
                    target_key = 'play_addr_lowbr'
                elif 'play_addr' in video_url_json.keys():
                    target_key = 'play_addr'
                else:
                    continue
                video_url = data_json['aweme_list'][i]['video'][target_key]['url_list'][0]

                video_name = re.sub(rstr, '', data_json['aweme_list'][i]['desc'])

                parsed_urls_names.append([video_url, video_name])
            while has_more == True:
                url_parsed = parse.urlparse(url)
                bits = list(url_parsed)
                qs = parse.parse_qs(bits[4])
                qs['max_cursor'] = max_cursor
                bits[4] = parse.urlencode(qs, True)

                # 重新拼接整个url,只要hasmore是否为true，则反复访问作者主页链接，直到成功返回这个为false
                url_new = parse.urlunparse(bits)
                r = requests.get(url=url_new, headers=self.headers, stream=True)
                data_json = json.loads(r.text)
                has_more = data_json['has_more']  # 重置hasmore直到返回为false则退出循环
                max_cursor = data_json['max_cursor']  # 每次重置这个页数，继续替换url中下一页页码进行访问
                for i in range(len(data_json['aweme_list'])):
                    video_url_json = data_json['aweme_list'][i]['video']
                    target_key = ""
                    if 'play_addr_lowbr' in video_url_json.keys():
                        target_key = 'play_addr_lowbr'
                    elif 'play_addr' in video_url_json.keys():
                        target_key = 'play_addr'
                    else:
                        continue
                    video_url = data_json['aweme_list'][i]['video'][target_key]['url_list'][0]
                    video_name = re.sub(rstr, '', data_json['aweme_list'][i]['desc'])

                    parsed_urls_names.append([video_url, video_name])
        except:
            pass

        nickname = str(time.time())
        if len(nicknames) != 0:
            nickname = nicknames[0]


        return nickname, parsed_urls_names

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
