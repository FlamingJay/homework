import datetime
import multiprocessing

import win_unicode_console
from moviepy.editor import concatenate_videoclips, afx, AudioFileClip, ImageClip, CompositeVideoClip
from VideoProcess import single_process

import sys
import os
from PyQt5.QtWidgets import (QWidget, QRadioButton, QPushButton, QLineEdit, QLabel, QApplication, QFileDialog, QListWidget, QListWidgetItem, QTextEdit, QTextBrowser)
from moviepy.video.io.VideoFileClip import VideoFileClip
win_unicode_console.enable()


class login(QWidget):
    def __init__(self):
        super(login, self).__init__()
        self.background_pic = None
        self.pic_width = 1920
        self.pic_height = 1080
        self.background_audio = None
        self.audio_vol = 100

        self.func1_input_path = None
        self.func1_output_path = None

        self.func2_videos = []
        self.func2_file_list = []
        self.func2_duration_list = []
        self.func2_total_duration = 0
        self.func2_del_videos_idx = []

        self.func2_output_path = None
        self.func2_item_count = 0

        self.initUI()

    def initUI(self):

        # 背景图和相关配置
        self.picture_btn = QPushButton('背景图', self)
        self.picture_btn.move(30, 30)
        self.picture_btn.resize(60, 30)
        self.picture_btn.clicked.connect(self.__select_picture)
        self.picture_le = QTextBrowser(self)
        self.picture_le.move(120, 30)
        self.picture_le.resize(250, 30)

        self.width_text = QLabel('宽度：', self)
        self.width_text.move(400, 30)
        self.width_text.resize(30, 30)

        self.width_edit = QLineEdit("1920", self)
        self.width_edit.move(450, 30)
        self.width_edit.resize(40, 30)
        self.pic_width = int(self.width_edit.text())

        self.height_text = QLabel('高度：', self)
        self.height_text.move(500, 30)
        self.height_text.resize(30, 30)

        self.height_edit = QLineEdit("1080", self)
        self.height_edit.move(550, 30)
        self.height_edit.resize(40, 30)
        self.pic_height = int(self.height_edit.text())

        # 背景乐
        self.audio_btn = QPushButton('背景乐', self)
        self.audio_btn.move(30, 90)
        self.audio_btn.resize(60, 30)
        self.audio_btn.clicked.connect(self.__select_audio)
        self.audio_le = QTextBrowser(self)
        self.audio_le.move(120, 90)
        self.audio_le.resize(250, 30)

        self.volume_text = QLabel('音量：', self)
        self.volume_text.move(400, 90)
        self.volume_text.resize(30, 30)
        self.volume = QTextEdit("100", self)
        self.volume.move(450, 90)
        self.volume.resize(40, 30)

        # 功能1：自动剪辑
        self.func1 = QLabel('功能1：自动编辑', self)
        self.func1.move(30, 150)
        self.func1.resize(90, 30)

        self.front_text = QLabel('片头：', self)
        self.front_text.move(30, 180)
        self.front_text.resize(30, 30)
        self.front = QTextEdit("0", self)
        self.front.move(70, 180)
        self.front.resize(30, 30)

        self.end_text = QLabel('片尾：', self)
        self.end_text.move(110, 180)
        self.end_text.resize(30, 30)
        self.end = QTextEdit("0", self)
        self.end.move(150, 180)
        self.end.resize(30, 30)

        self.water_text = QLabel('水印：', self)
        self.water_text.move(250, 180)
        self.water_text.resize(30, 30)
        self.water_logo = QTextBrowser(self)
        self.water_logo.move(300, 180)
        self.water_logo.resize(230, 30)

        # 原视频，用于拼接
        self.func1_input_path_btn = QPushButton('原视频目录', self)
        self.func1_input_path_btn.move(30, 220)
        self.func1_input_path_btn.resize(70, 30)
        self.func1_input_path_btn.clicked.connect(self.__select_func1_input_path)
        self.func1_input_path_text = QTextBrowser(self)
        self.func1_input_path_text.move(120, 220)
        self.func1_input_path_text.resize(250, 30)

        self.func1_save_path_btn = QPushButton('保存目录', self)
        self.func1_save_path_btn.move(30, 260)
        self.func1_save_path_btn.resize(70, 30)
        self.func1_save_path_btn.clicked.connect(self.__select_func1_output_path)
        self.func1_save_path_text = QTextBrowser(self)
        self.func1_save_path_text.move(120, 260)
        self.func1_save_path_text.resize(250, 30)

        self.func1_run_btn = QPushButton('运行', self)
        self.func1_run_btn.move(460, 220)
        self.func1_run_btn.resize(70, 70)
        self.func1_run_btn.clicked.connect(self.__func1_run)


        # 功能2：合集
        self.func2 = QLabel('功能2：合集', self)
        self.func2.move(30, 320)
        self.func2.resize(90, 30)

        # 选取视频
        self.func2_input_path_btn = QPushButton('原视频', self)
        self.func2_input_path_btn.move(30, 350)
        self.func2_input_path_btn.resize(70, 30)
        self.func2_input_path_btn.clicked.connect(self.__select_func2_input)
        self.func2_input_path_text = QTextBrowser(self)
        self.func2_input_path_text.move(120, 350)
        self.func2_input_path_text.resize(250, 30)

        # 显示选取视频的总时长
        self.func2_total_dur_title = QLabel('所选视频总时长：', self)
        self.func2_total_dur_title.move(400, 350)
        self.func2_total_dur_title.resize(90, 30)
        self.func2_total_dur_view = QLabel(self)
        self.func2_total_dur_view.move(500, 340)
        self.func2_total_dur_view.resize(200, 50)

        # 列表
        self.func2_list_widget = QListWidget(self)
        self.func2_list_widget.move(30, 400)
        self.func2_list_widget.resize(600, 320)

        # 添加按钮
        self.func2_add_btn = QPushButton('+', self)
        self.func2_add_btn.move(630, 400)
        self.func2_add_btn.resize(30, 30)
        self.func2_add_btn.clicked.connect(self.__add_item)

        # 删除按钮
        self.func2_del_btn = QPushButton('-', self)
        self.func2_del_btn.move(630, 450)
        self.func2_del_btn.resize(30, 30)
        self.func2_del_btn.clicked.connect(self.__remove_row)

        # 保存按钮，调取数据增加函数等
        self.func2_save_path_btn = QPushButton('存储路径', self)
        self.func2_save_path_btn.move(30, 730)
        self.func2_save_path_btn.resize(60, 30)
        self.func2_save_path_btn.clicked.connect(self.__select_func2_output_path)
        self.func2_save_path_text = QTextBrowser(self)
        self.func2_save_path_text.move(120, 730)
        self.func2_save_path_text.resize(250, 30)

        # 剪辑
        self.work_btn = QPushButton('合集', self)
        self.work_btn.move(540, 730)
        self.work_btn.resize(90, 30)
        self.work_btn.clicked.connect(self.__func2_run)

        # 整体界面设置
        self.setGeometry(800, 400, 700, 800)
        self.setWindowTitle('视频剪切')  # 设置界面标题名
        self.show()


    def __select_func1_input_path(self):
        self.func1_input_path = QFileDialog.getExistingDirectory(self, "选择视频路径", "E:/")
        self.func1_input_path_text.setText(self.func1_input_path)

    def __select_func1_output_path(self):
        self.func1_output_path = QFileDialog.getExistingDirectory(self, "选择保存目录", "E:/")
        self.func1_save_path_text.setText(self.func1_output_path)

    # 选择背景图
    def __select_picture(self):
        self.background_pic, fileType = QFileDialog.getOpenFileName(self, "选择源文件", "E:/")
        self.picture_le.setText(str(self.background_pic))

    # 选择背景乐
    def __select_audio(self):
        self.background_audio, fileType = QFileDialog.getOpenFileName(self, "选择源文件", "E:/")
        self.audio_le.setText(str(self.background_audio))

    def __select_func2_input(self):
        self.__reset_func2_input()
        targets, fileTypes = QFileDialog.getOpenFileNames(self, "选择源文件", r"E:\homeWork\editor\demo")
        self.func2_input_path_text.setText("/".join(targets[0].split("/")[:-1]))
        self.func2_file_list = targets
        self.__func2_preprocess()

    def __select_func2_output_path(self):
        self.func2_output_path = QFileDialog.getExistingDirectory(self, "选择保存目录", "E:/")
        self.func2_save_path_text.setText(self.func2_output_path)

    def __func1_run(self):
        '''
        自动剪辑
        :return:
        '''
        videos = []
        names = []
        # 目录下所有的文件
        files = os.listdir(self.func1_input_path)
        if len(files) < 1:
            assert "重新选择"
        for file in files:
            videos.append(self.func1_input_path + "/" + file)
            names.append(file.split("/")[-1])

        count = len(videos)
        muisic = [self.background_audio] * count
        pic = [self.background_pic] * count
        save_path = [self.func1_output_path] * count
        width = [int(self.pic_width)] * count
        height = [int(self.pic_height)] * count

        # 对每一个视频都做同样的操作
        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            pool.map(single_process, zip(videos, names, muisic, pic, save_path, width, height))

        self.__reset_func1()
        self.__reset_common()

    # 预处理
    def __func2_preprocess(self):
        # 计算总时长,显示列表
        for file in self.func2_file_list:
            xx = VideoFileClip(file)
            duration = xx.duration
            self.func2_videos.append(xx)
            self.func2_duration_list.append(duration)
            self.func2_total_duration += duration
            # 添加 index | 时长 |名字
            item = QListWidgetItem()
            item.setText(str(self.func2_item_count) + "   |   " + str(duration) + "秒   |   " + file.split("/")[-1])
            item.setWhatsThis(str(self.func2_item_count))
            self.func2_list_widget.addItem(item)

            self.func2_item_count += 1

        self.func2_total_dur_view.setText(str(self.func2_total_duration).format("%.1f") + "秒")
        self.func2_total_dur_view.setStyleSheet("color:red;font-size:24px")
        self.func2_total_dur_view.update()

    def __func2_run(self):
        '''
        合集
        :return:
        '''
        # 拼接
        videos = []
        if len(self.func2_videos) > 0:
            for idx, video in enumerate(self.func2_videos):
                if str(idx) not in self.func2_del_videos_idx:
                    videos.append(video)

        del self.func2_videos
        if len(videos) < 1:
            assert "重新选择"

        res = concatenate_videoclips(videos)
        # 背景乐
        if self.background_audio is not None:
            res = res.without_audio()

            audio_clip = AudioFileClip(self.background_audio)
            audio = afx.audio_loop(audio_clip, duration=self.func2_total_duration)
            res = res.set_audio(audio)

        # 背景图
        if self.background_pic is not None:
            res = res.set_position('center')
            background_clip = ImageClip(self.background_pic)
            background_clip = background_clip.set_pos('center').set_duration(self.func2_total_duration)
            # 编辑图片的尺寸
            background_clip = background_clip.resize((self.pic_width, self.pic_height))
            # 叠层
            res = CompositeVideoClip([background_clip, res])

        # 写入
        cur_time = datetime.date.today()
        # 加弹窗
        if self.func2_output_path is not None:
            res.write_videofile(self.func2_output_path + "\\" + str(cur_time) + ".mp4")
        else:
            res.write_videofile(os.path.dirname(sys.executable) + "\\" + str(cur_time) + ".mp4")

        self.__reset_func2()
        self.__reset_common()

    def __reset_func1(self):
        self.func1_input_path = None
        self.func1_input_path_text.setText("")
        self.func1_output_path = None
        self.func1_save_path_text.setText("")

    def __reset_func2(self):
        self.func2_videos = []
        self.func2_file_list = []
        self.func2_duration_list = []
        self.func2_total_duration = 0
        self.func2_item_count = 0
        self.func2_del_videos_idx = []

        self.func2_output_path = None
        self.func2_save_path_text.setText("")


        self.func2_list_widget.clear()

    def __reset_func2_input(self):
        self.func2_videos = []
        self.func2_file_list = []
        self.func2_duration_list = []
        self.func2_total_duration = 0
        self.func2_del_videos_idx = []
        self.func2_list_widget.clear()

    def __reset_common(self):
        '''
        重置
        :return:
        '''
        self.background_pic = None
        self.picture_le.setText("")

        self.pic_width = 1920
        self.pic_height = 1080
        self.background_audio = None
        self.audio_le.setText("")
        self.audio_vol = 100

    def __add_item(self):
        # 打开文件
        video, fileType = QFileDialog.getOpenFileName(self, "添加文件", "E:/")

        # 添加
        xx = VideoFileClip(video)
        duration = xx.duration
        self.func2_videos.append(xx)
        self.func2_duration_list.append(duration)
        self.func2_total_duration += duration
        # 添加 index | 时长 |名字
        item = QListWidgetItem()
        item.setText(str(self.func2_item_count) + "   |   " + str(duration) + "秒   |   " + video)
        item.setWhatsThis(str(self.func2_item_count))
        self.func2_list_widget.addItem(item)

        self.func2_item_count += 1
        self.func2_total_dur_view.setText(str(self.func2_total_duration).format("%.1f") + "秒")
        self.func2_total_dur_view.setStyleSheet("color:red;font-size:24px")
        self.func2_total_dur_view.update()

    def __remove_row(self):
        item = self.func2_list_widget.currentItem()
        index = item.whatsThis()
        self.func2_list_widget.takeItem(self.func2_list_widget.row(item))
        # 把下标存起来
        self.func2_del_videos_idx.append(index)
        # 更新总时长
        cur_duration = self.func2_duration_list[int(index)]
        self.func2_total_duration -= cur_duration
        self.func2_total_dur_view.setText(str(self.func2_total_duration).format("%.1f") + "秒")
        self.func2_total_dur_view.setStyleSheet("color:red;font-size:24px")
        self.func2_total_dur_view.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = login()
    sys.exit(app.exec_())