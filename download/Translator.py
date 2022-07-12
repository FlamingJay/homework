import re
import hashlib
import random
import requests
from importlib import resources


def word_replace(text, word_dict):
    text = re.sub('[^\u4e00-\u9fa5^a-z^A-Z^0-9\.\_ ]', '', text)
    for key in word_dict.keys():
        if key in text:
            text.replace(key, word_dict[key])

    return text


def load_word_dict():
    word_dict = dict()
    with resources.open_text("resource", "word_dict.txt") as f:
        for line in f.readlines():
            token = line.split("|")
            word_dict[token[0]] = token[1]
    return word_dict


def baiduAPI_translate(query_str, from_lang, to_lang):
    '''
    传入待翻译的字符串和目标语言类型，请求 apiURL，自动检测传入的语言类型获得翻译结果
    :param query_str: 待翻译的字符串
    :param from_lang: 当前语言类型
    :param to_lang: 目标语言类型
    :return: 翻译结果字典
    '''
    apiURL = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    appID = '20220621001253515'
    secretKey = 'TbZ9GHaoAsbKcZDLz8oT'
    # 生成随机的 salt 值
    salt = str(random.randint(32768, 65536))
    # 准备计算 sign 值需要的字符串
    pre_sign = appID + query_str + salt + secretKey
    # 计算 md5 生成 sign
    sign = hashlib.md5(pre_sign.encode()).hexdigest()
    # 请求 apiURL 所有需要的参数
    params = {
        'q': query_str,
        'from': from_lang,
        'to': to_lang,
        'appid': appID,
        'salt': salt,
        'sign': sign
    }
    try:
        # 直接将 params 和 apiURL 一起传入 requests.get() 函数
        response = requests.get(apiURL, params=params)
        # 获取返回的 json 数据
        result_dict = response.json()
        # 得到的结果正常则 return
        if 'trans_result' in result_dict:
            res = result_dict['trans_result'][0]['dst']
            # 过滤
            res = re.sub(r'[\\/:*?<>？]', r'../qt', res)[0: min(len(res), 250)]
            return res
        else:
            return query_str
    except Exception as e:
        return query_str
