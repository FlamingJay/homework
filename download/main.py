import tkinter as tk  # 使用Tkinter前需要先导入
from tkinter.ttk import Combobox
from animationLabel import MyLabel
from getDouYinV2 import getDouYin
import tkinter.messagebox
from tkinter.filedialog import askdirectory
import time
import frozen
from tklog import tklog

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

        # 保存路径
        self.var_save_name = tk.StringVar()
        self.var_save_name.set('')
        entry_save_name = tk.Entry(self.window, textvariable=self.var_save_name, font=('宋体', 20))
        entry_save_name.place(x=250, y=230, height=30, width=250)
        btn_path = tk.Button(self.window, text='路径选择', command=self.__select_path, font=('宋体', 10))
        btn_path.place(x=550, y=230, height=35, width=70)

        # 下载
        btn_download = tk.Button(self.window, text='下载', command=self.__download, height=1, width=40, bg='green', font=('宋体',20))
        btn_download.place(x=100, y=310)

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
            # self.autoloader = getYouTube()
            self.eblog.log(time.strftime('%Y-%m-%d %H:%M:%S %A') + "创建youtube下载器")
            self.eblog.update()
            tk.messagebox.showerror(title='hey', message='先用抖音douyin那个！')
        else:
            self.autoloader = None
            tk.messagebox.showerror(title='hey', message='先用抖音douyin那个！')

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

            isOver = self.autoloader.download(target_link, save_path, self.eblog)
            if isOver:
                tk.messagebox.showinfo(title='hey', message='下载完成啦！')

    def run(self):
        self.eblog.log(time.strftime('%Y-%m-%d %H:%M:%S %A') + "------------开始执行程序")
        self.window.mainloop()


if __name__ == "__main__":
    loop = shortVideo()
    loop.run()