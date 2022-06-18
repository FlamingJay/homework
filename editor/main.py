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
        # self.pic_width = 1920
        # self.pic_height = 1080
        # 视频裁剪的起点、宽度和高度
        self.crop_point = dict()
        self.crop_point["crop_x_start"] = 0
        self.crop_point["crop_y_start"] = 0
        self.crop_point["crop_x_end"] = 0
        self.crop_point["crop_y_end"] = 0
        self.background_audio = None
        self.audio_vol = 100
        self.water_logo = None

        self.func1_input_path = None
        self.func1_output_path = None
        self.front_cut_dur = 0
        self.end_cut_dur = 0

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

        # self.width_text = QLabel('宽度：', self)
        # self.width_text.move(400, 30)
        # self.width_text.resize(30, 30)
        #
        # self.width_edit = QLineEdit("1920", self)
        # self.width_edit.move(450, 30)
        # self.width_edit.resize(40, 30)
        # self.pic_width = int(self.width_edit.text())
        #
        # self.height_text = QLabel('高度：', self)
        # self.height_text.move(500, 30)
        # self.height_text.resize(30, 30)
        #
        # self.height_edit = QLineEdit("1080", self)
        # self.height_edit.move(550, 30)
        # self.height_edit.resize(40, 30)
        # self.pic_height = int(self.height_edit.text())

        # 背景乐
        self.audio_btn = QPushButton('背景乐', self)
        self.audio_btn.move(30, 70)
        self.audio_btn.resize(60, 30)
        self.audio_btn.clicked.connect(self.__select_audio)
        self.audio_le = QTextBrowser(self)
        self.audio_le.move(120, 70)
        self.audio_le.resize(250, 30)

        self.volume_text = QLabel('音量：', self)
        self.volume_text.move(400, 70)
        self.volume_text.resize(30, 30)
        self.volume = QTextEdit("100", self)
        self.volume.move(450, 70)
        self.volume.resize(40, 30)

        # 水印
        self.water_btn = QPushButton('水印', self)
        self.water_btn.move(30, 110)
        self.water_btn.resize(60, 30)
        self.water_btn.clicked.connect(self.__select_water_pic)
        self.water_le = QTextBrowser(self)
        self.water_le.move(120, 110)
        self.water_le.resize(250, 30)

        # 功能1：自动剪辑
        self.func1 = QLabel('功能1：自动编辑', self)
        self.func1.move(30, 150)
        self.func1.resize(90, 30)

        self.front_text = QLabel('片头：', self)
        self.front_text.move(30, 180)
        self.front_text.resize(30, 30)
        self.front = QLineEdit("0", self)
        self.front.move(70, 180)
        self.front.resize(30, 30)
        self.front_cut_dur = int(self.front.text())

        self.end_text = QLabel('片尾：', self)
        self.end_text.move(110, 180)
        self.end_text.resize(30, 30)
        self.end = QLineEdit("0", self)
        self.end.move(150, 180)
        self.end.resize(30, 30)
        self.end_cut_dur = int(self.end.text())

        # 裁剪左上角坐标
        self.crop_x_start_text = QLabel('起点x：', self)
        self.crop_x_start_text.move(250, 180)
        self.crop_x_start_text.resize(40, 30)
        self.crop_x_start_line = QLineEdit("0", self)
        self.crop_x_start_line.move(300, 180)
        self.crop_x_start_line.resize(30, 30)
        self.crop_x_start_line.editingFinished.connect(lambda :self.__value_change("crop_x_start", self.crop_x_start_line.text()))

        self.crop_y_start_text = QLabel('起点y：', self)
        self.crop_y_start_text.move(340, 180)
        self.crop_y_start_text.resize(40, 30)
        self.crop_y_start_line = QLineEdit("0", self)
        self.crop_y_start_line.move(390, 180)
        self.crop_y_start_line.resize(30, 30)
        self.crop_y_start_line.editingFinished.connect(lambda :self.__value_change("crop_y_start", self.crop_y_start_line.text()))

        # 裁剪右下角坐标
        self.crop_x_end_text = QLabel('终点x：', self)
        self.crop_x_end_text.move(440, 180)
        self.crop_x_end_text.resize(40, 30)
        self.crop_x_end_edit = QLineEdit("0", self)
        self.crop_x_end_edit.move(490, 180)
        self.crop_x_end_edit.resize(40, 30)
        self.crop_x_end_edit.editingFinished.connect(lambda :self.__value_change("crop_x_end", self.crop_x_end_edit.text()))

        self.crop_y_end_text = QLabel('终点y：', self)
        self.crop_y_end_text.move(540, 180)
        self.crop_y_end_text.resize(40, 30)
        self.crop_y_end_edit = QLineEdit("0", self)
        self.crop_y_end_edit.move(580, 180)
        self.crop_y_end_edit.resize(40, 30)
        self.crop_y_end_edit.editingFinished.connect(lambda :self.__value_change("crop_y_end", self.crop_y_end_edit.text()))

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
        self.func1_run_btn.move(540, 220)
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

    def __value_change(self, target, val):
        self.crop_point[target] = val

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

    # 选择水印
    def __select_water_pic(self):
        self.water_logo, fileType = QFileDialog.getOpenFileName(self, "选择源文件", "E:/")
        self.water_le.setText(str(self.water_logo))

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
        # width = [int(self.pic_width)] * count
        # height = [int(self.pic_height)] * count
        crop_x_start = [int(self.crop_point["crop_x_start"])] * count
        crop_y_start = [int(self.crop_point["crop_y_start"])] * count
        crop_x_end = [int(self.crop_point["crop_x_end"])] * count
        crop_y_end = [int(self.crop_point["crop_y_end"])] * count
        water_logo = [self.water_logo] * count
        front_cut = [self.front_cut_dur] * count
        end_cut = [self.end_cut_dur] * count

        # 对每一个视频都做同样的操作
        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            pool.map(single_process, zip(videos, names, muisic, pic, save_path, crop_x_start, crop_y_start, crop_x_end, crop_y_end, water_logo, front_cut, end_cut))

        self.__reset_func1()
        self.__reset_common()

    # 预处理
    def __func2_preprocess(self):
        # 计算总时长,显示列表
        for file in self.func2_file_list:
            xx = VideoFileClip(file)

            xx = xx.subclip(self.front_cut_dur, xx.duration-self.end_cut_dur)
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

        all_videos = concatenate_videoclips(videos)
        all_videos = all_videos.set_position('center')

        # 背景乐
        if self.background_audio is not None:
            all_videos = all_videos.without_audio()

            audio_clip = AudioFileClip(self.background_audio)
            audio = afx.audio_loop(audio_clip, duration=self.func2_total_duration)
            all_videos = all_videos.set_audio(audio)

        # 背景图
        if self.background_pic is not None:

            background_clip = ImageClip(self.background_pic)
            background_clip = background_clip.set_pos('center').set_duration(self.func2_total_duration)
            back_size = background_clip.size

        if self.water_logo is not None:
            water_clip = ImageClip(self.water_logo)
            water_clip = water_clip.set_pos('center').set_duration(self.func2_total_duration)

        if (self.background_pic is not None) and (self.water_logo is not None):
            # 视频适配背景
            if back_size[0] > back_size[1]:
                new_height = 1080
                new_width = new_height * video.size[0] / video.size[1]
            else:
                new_width = 1080
                new_height = new_width * video.size[1] / video.size[0]
            all_videos = all_videos.resize((new_width, new_height))

            # 叠层
            res = CompositeVideoClip([background_clip, all_videos, water_clip])
        elif self.background_pic is not None:
            if back_size[0] > back_size[1]:
                new_height = 1080
                new_width = new_height * video.size[0] / video.size[1]
            else:
                new_width = 1080
                new_height = new_width * video.size[1] / video.size[0]
            all_videos = all_videos.resize((new_width, new_height))

            res = CompositeVideoClip([background_clip, all_videos])
        elif self.water_logo is not None:
            res = CompositeVideoClip([all_videos, water_clip])

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
        self.crop_point["crop_x_start"] = 0
        self.crop_point["crop_y_start"] = 0
        self.crop_point["crop_x_end"] = 0
        self.crop_point["crop_y_end"] = 0
        self.crop_x_start_line.setText("0")
        self.crop_x_end_edit.setText("0")
        self.crop_y_start_line.setText("0")
        self.crop_y_end_edit.setText("0")
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

        # self.pic_width = 1920
        # self.pic_height = 1080
        self.background_audio = None
        self.audio_le.setText("")
        self.audio_vol = 100

        self.water_logo = None

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