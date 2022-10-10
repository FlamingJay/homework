import base64
import os
import re
import json
from abc import ABC
from contextlib import closing

import requests
import execjs
from download.AutoDownLoader import AutoDownLoader


class XiguaDownloader(AutoDownLoader, ABC):
	def __init__(self):
		self.headers = {
			'cookie': 'MONITOR_WEB_ID=7150929952647857694; _tea_utm_cache_1300=undefined; ttcid=9139c6381f264f9a86cc469db71f199175; tt_scid=4CzxxBHxx1AS02YjYeBt02rYO-ND2OakT3radlgp0hWaCoexwq21s0IZG33gjiqbf15e; ttwid=1|kVHm9rjcb53HgfkrmPeje_kkgLE6eOnYRBXy5glhBVA|1665033558|5ec3f1ac64e101e0691fa45db8970d6fe745a507bc503c7c00fdc60c801bf70d; ixigua-a-s=1; support_webp=true; support_avif=true; msToken=AnKS6IXLYfOLuSzU2Ybe284UDs7A5ajpoJbPLgUPWSJ0rK_giD5a-zPDZMCsgCfB7sbgHGN9Aw-ZIjvUVd4hJYDnn4uss9eCEd5t40Zo8fIxw1qsH-KdVbqBKHaIEQ==; __ac_nonce=0633fe01c009f6114a905; __ac_signature=_02B4Z6wo00f0110WMLwAAIDA7efcdOXABpddNjQAALSFZOdX4FOlsjRQXj1O.RlxQhDlP0KodZ2TWD50YUSs02uWj.Nb4iAemr.M8ZFKWXbND2yJ810BpXynPCtpl-5gi.2OeKmVnx7GGTshcd; __ac_referer=__ac_blank',
			'referer': 'https://www.ixigua.com/',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
		}

	def parseUrl(self, home_page_url):
		home_resp = requests.get(home_page_url, headers=self.headers)
		home_resp.encoding = 'utf-8'
		home_html = home_resp.text

		# 获取主页视频总数量，主页昵称
		video_total_count = re.findall('"video_total_count":"(.*?)"', home_html)[0]

		nickname = re.findall('<title data-react-helmet="true">(.*)的个人主页 - 西瓜视频</title>', home_html)[0]
		user_id = home_page_url.split("/")[4]

		# 反爬出签名
		path = os.path.join(os.path.dirname(__file__), "xigua.js")
		jscode = execjs.compile(open(path).read())
		nonce = home_resp.cookies.get("__ac_nonce")
		ctx = jscode.call("getSign", nonce, home_page_url)
		signature = ctx

		# 真正的存储视频的地址
		url = 'https://www.ixigua.com/api/videov2/author/new_video_list?to_user_id={0}&offset=0&limit={1}&_signature={2}'\
			.format(user_id, video_total_count, signature)
		video_html = requests.get(url, headers=self.headers)
		video_html.encoding = 'utf-8'
		json_video = video_html.text
		json_video_data = json.loads(json_video)
		video_list = json_video_data['data']['videoList']

		# 得到所有视频的id
		group_ids = [item['group_id'] for item in video_list]

		parsed_urls_names = []
		# 标题正则修改
		rstr = r"[\/\\\:;\*#￥%$!@^……&()\?\"\<\>\|\n\t]"
		for id in set(group_ids):
			# 视频下载地址（伪装）
			url = 'https://www.ixigua.com/{}'.format(id)

			resp = requests.get(url, headers=self.headers)
			resp.encoding = 'utf-8'

			res_html = resp.text
			json_str = re.findall('window._SSR_HYDRATED_DATA=(.*?)</script>', res_html)[0]
			json_str = json_str.replace('undefined', 'null')
			json_data = json.loads(json_str)
			video_name = re.sub(rstr, "", json_data['anyVideo']['gidInformation']['packerData']['video']['title'])
			video_list = json_data['anyVideo']['gidInformation']['packerData']['video']['videoResource']['normal']['video_list']
			for i in ['5', '4', '3', '2', '1']:
				video_n = 'video_' + i
				if video_n in video_list.keys():
					main_url = video_list[video_n]['main_url']
					break

			video_url = base64.b64decode(main_url).decode()
			print("{0}:{1}".format(video_name, video_url))
			parsed_urls_names.append([video_url, video_name])

		return nickname, parsed_urls_names

	def download(self, video_url, video_name, save_path):
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
