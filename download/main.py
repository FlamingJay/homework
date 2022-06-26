import os
import tkinter as tk
from tkinter.ttk import Combobox

from animationLabel import MyLabel
from getDouYinV2 import getDouYin
from getYoutube import getYoutube
import tkinter.messagebox
from tkinter.filedialog import askdirectory
import time
import frozen
from tklog import tklog

import re
import hashlib
import random
import requests

class shortVideo():
    def __init__(self):
        # 第0步，创建一个下载器对象
        self.autoloader = None

        # 第1步，实例化object，建立窗口window，加载动图，
        self.window = tk.Tk()

        anim = MyLabel(self.window, frozen.resource_path('gif') + r'\xx.gif')
        anim.place(x=650, y=80)

        # 第2步，创建日志控件
        self.eblog = tklog(master=self.window)
        self.eblog.place(x=100, y=400, height=200, width=590)

        # 第3步，给窗口的可视化起名字，设定窗口大小
        self.window.title('搬起来，运出去')
        self.window.geometry('850x700')  # 这里的乘是小x

        # 第4步，标题
        tk.Label(self.window, text='网站', font=('宋体', 14)).place(x=100, y=70)
        tk.Label(self.window, text='主页链接', font=('宋体', 14)).place(x=100, y=150)
        tk.Label(self.window, text='保存路径', font=('宋体', 14)).place(x=100, y=230)

        # 第5步，输入
        # 网站
        self.website = tk.StringVar()
        w = Combobox(self.window, textvariable=self.website)
        w['values'] = ("tiktok", "douyin", "youtube")  # 设置下拉列表的值
        w.place(x=250, y=70, height=30, width=250)

        btn_confirm = tk.Button(self.window, text='确认', command=self.__confirm_web)
        btn_confirm.place(x=550, y=70, height=35, width=70)

        # 主页链接
        self.var_home_name = tk.StringVar()
        self.var_home_name.set('')
        entry_home_name = tk.Entry(self.window, textvariable=self.var_home_name, font=('宋体', 20))
        entry_home_name.place(x=250, y=150, height=30, width=250)

        # 是否翻译成英文标题
        self.translate_to_english = False
        self.val = tk.IntVar()
        english_btn = tk.Checkbutton(self.window, text="英文标题", command=self.__click, variable=self.val)
        english_btn.place(x=530, y=150, height=30, width=100)


        # 保存路径
        self.var_save_name = tk.StringVar()
        self.var_save_name.set('')
        entry_save_name = tk.Entry(self.window, textvariable=self.var_save_name, font=('宋体', 20))
        entry_save_name.place(x=250, y=230, height=30, width=250)
        btn_path = tk.Button(self.window, text='路径选择', command=self.__select_path, font=('宋体', 10))
        btn_path.place(x=550, y=230, height=35, width=70)

        # 下载
        btn_download = tk.Button(self.window, text='下载', command=self.__download, height=1, width=40, bg='green',
                                 font=('宋体', 20))
        btn_download.place(x=100, y=310)

    def __click(self):
        if self.val.get() == 0:
            self.translate_to_english = False
        else:
            self.translate_to_english = True

    def __confirm_web(self):
        '''
        确认是哪一个网站
        :return:
        '''
        web = self.website.get()
        if web == "douyin":
            self.eblog.log(time.strftime('%Y-%m-%d %H:%M:%S %A') + "------------创建douyin下载器")
            self.eblog.update()
            # 创建下载器
            self.autoloader = getDouYin()
        elif web == 'youtube':
            self.autoloader = getYoutube()
            self.eblog.log(time.strftime('%Y-%m-%d %H:%M:%S %A') + "创建youtube下载器")
            self.eblog.update()

        else:
            self.autoloader = None
            tk.messagebox.showerror(title='hey', message='tiktok还不太行呢')

    def __select_path(self):
        '''
        选择路径
        :return:
        '''
        self.eblog.log(time.strftime('%Y-%m-%d %H:%M:%S %A') + "------------存储路径选择")
        self.eblog.update()
        _path = askdirectory()
        self.var_save_name.set(_path)

    def __download(self):
        '''
        下载
        :return:
        '''
        self.eblog.log(time.strftime('%Y-%m-%d %H:%M:%S %A') + "------------执行下载程序")
        self.eblog.update()
        target_link = self.var_home_name.get()
        save_path = self.var_save_name.get()
        if self.autoloader is None:
            tk.messagebox.showerror(title='hey', message='忘记选择网站了！')
        elif target_link == "":
            tk.messagebox.showerror(title='hey', message='忘记填写主页链接了！')
        elif save_path == "":
            tk.messagebox.showerror(title='hey', message='忘记填写保存路径了！')
        else:

            isOver, files_path = self.autoloader.download(target_link, save_path, self.eblog)
            if isOver:
                # 重命名
                if self.translate_to_english:
                    files = os.listdir(files_path)

                    for file in files:
                        old = files_path + os.sep + file
                        # file文本替换
                        new_file = self.word_replace(file)
                        time.sleep(1)
                        print(new_file)
                        names = new_file.split(".")
                        if len(names) == 2:
                            new = files_path + os.sep + self.baiduAPI_translate(query_str=names[0], from_lang='zh',
                                                                            to_lang='en') + "." + names[1]
                        else:
                            new = new_file

                        while os.path.exists(new):
                            names = new.split(".")
                            if len(names) == 2:
                                new = names[0] + "_." + names[1]
                        os.rename(old, new)

                tk.messagebox.showinfo(title='hey', message='下载完成啦！')

    def word_replace(self, text):
        word_dict = self.load_word_dict()
        text = re.sub('[^\u4e00-\u9fa5^a-z^A-Z^0-9\.\_]', '', text)
        for key in word_dict.keys():
            if key in text:
                text.replace(key, word_dict[key])

        return text

    def load_word_dict(self):
        word_dict = dict()
        with open("./resource/word_dict.txt", "r", encoding='utf-8') as f:
            for line in f.readlines():
                token = line.split("|")
                word_dict[token[0]] = token[1]
        return word_dict

    def baiduAPI_translate(self, query_str, from_lang, to_lang):
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
            print(result_dict)
            # 得到的结果正常则 return
            if 'trans_result' in result_dict:
                return result_dict['trans_result'][0]['dst']
            else:
                return query_str
        except Exception as e:
            return query_str

    def run(self):
        self.eblog.log(time.strftime('%Y-%m-%d %H:%M:%S %A') + "------------开始执行程序")
        self.window.mainloop()


if __name__ == "__main__":
    loop = shortVideo()
    loop.run()
