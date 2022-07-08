# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\shortVideo.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem
from DownloadThread import DownloadThread
from qt.EditorThread import EditorThread

from Params import *


class Ui_MainWindow(object):

    def __init__(self):
        self.download_params = dict()
        for key in Params.download_keys:
            self.download_params[key] = None

        self.editor_parmas = dict()
        for key in Params.editor_common_keys:
            self.editor_parmas[key] = None
        for key in Params.single_editor_keys:
            self.editor_parmas[key] = None
        for key in Params.merge_editor_keys:
            self.editor_parmas[key] = None

        self.upload_parmas = dict()
        for key in Params.upload_keys:
            self.upload_parmas[key] = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1167, 886)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.group_box_upload = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box_upload.setGeometry(QtCore.QRect(20, 670, 1131, 161))
        self.group_box_upload.setObjectName("group_box_upload")
        self.account_table = QtWidgets.QTableWidget(self.group_box_upload)
        self.account_table.setGeometry(QtCore.QRect(10, 20, 1071, 131))
        self.account_table.setStyleSheet("color:rgb(0, 0, 0)")
        self.account_table.setObjectName("account_table")
        self.account_table.setColumnCount(9)
        self.account_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.account_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.account_table.setHorizontalHeaderItem(8, item)

        self.add_account_btn = QtWidgets.QPushButton(self.group_box_upload)
        self.add_account_btn.setGeometry(QtCore.QRect(1080, 20, 31, 23))
        self.add_account_btn.setObjectName("add_account_btn")


        self.delete_account_btn = QtWidgets.QPushButton(self.group_box_upload)
        self.delete_account_btn.setGeometry(QtCore.QRect(1080, 50, 31, 23))
        self.delete_account_btn.setObjectName("delete_account_btn")

        self.group_box_download = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box_download.setGeometry(QtCore.QRect(20, 110, 1131, 121))
        self.group_box_download.setMinimumSize(QtCore.QSize(0, 0))
        self.group_box_download.setSizeIncrement(QtCore.QSize(0, 0))
        self.group_box_download.setStyleSheet("border-color: rgb(255, 0, 0);")
        self.group_box_download.setObjectName("group_box_download")

        # 选择网站
        self.pick_web = QtWidgets.QComboBox(self.group_box_download)
        self.pick_web.setGeometry(QtCore.QRect(100, 30, 291, 31))
        self.pick_web.setObjectName("pick_web")
        self.pick_web.addItem("")
        self.pick_web.addItem("")

        # 确认网站
        self.web_confirm_btn = QtWidgets.QPushButton(self.group_box_download)
        self.web_confirm_btn.setGeometry(QtCore.QRect(440, 30, 75, 31))
        self.web_confirm_btn.setObjectName("web_confirm_btn")
        self.web_confirm_btn.clicked.connect(self.__confirm_web)

        # 主页链接
        self.input_home_url = QtWidgets.QLineEdit(self.group_box_download)
        self.input_home_url.setGeometry(QtCore.QRect(680, 30, 291, 31))
        self.input_home_url.setObjectName("input_home_url")
        self.input_home_url.editingFinished.connect(
            lambda: self.__line_edit_change("download", "home_page_url", self.input_home_url.text()))

        # label
        self.label_web = QtWidgets.QLabel(self.group_box_download)
        self.label_web.setGeometry(QtCore.QRect(20, 40, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setKerning(True)
        self.label_web.setFont(font)
        self.label_web.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_web.setObjectName("label_web")
        self.label_url = QtWidgets.QLabel(self.group_box_download)
        self.label_url.setGeometry(QtCore.QRect(590, 40, 54, 12))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_url.setFont(font)
        self.label_url.setObjectName("label_url")

        self.label_save_path_download = QtWidgets.QLabel(self.group_box_download)
        self.label_save_path_download.setGeometry(QtCore.QRect(20, 90, 54, 12))
        self.label_save_path_download.setObjectName("label_save_path_download")

        # 是否翻译成英文标题
        self.is_english_title = QtWidgets.QCheckBox(self.group_box_download)
        self.is_english_title.setGeometry(QtCore.QRect(1000, 40, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.is_english_title.setFont(font)
        self.is_english_title.setObjectName("is_english_title")
        self.download_params["translate_to_english"] = False
        self.is_english_title.clicked.connect(self.__translate_to_english)

        # 保存目录
        self.download_save_btn = QtWidgets.QPushButton(self.group_box_download)
        self.download_save_btn.setGeometry(QtCore.QRect(440, 80, 75, 31))
        self.download_save_btn.setObjectName("download_save_btn")
        self.download_save_btn.clicked.connect(lambda: self.__select_save_path("download", "save_path"))

        # 开始下载
        self.download_btn = QtWidgets.QPushButton(self.group_box_download)
        self.download_btn.setGeometry(QtCore.QRect(590, 80, 61, 31))
        self.download_btn.setObjectName("download_btn")
        self.download_btn.clicked.connect(self.__download_thread)
        self.download_save_display = QtWidgets.QTextBrowser(self.group_box_download)
        self.download_save_display.setGeometry(QtCore.QRect(100, 80, 291, 31))
        self.download_save_display.setObjectName("download_save_display")

        # 下载进度
        self.download_progress_bar = QtWidgets.QProgressBar(self.group_box_download)
        self.download_progress_bar.setGeometry(QtCore.QRect(680, 80, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.download_progress_bar.setFont(font)
        self.download_progress_bar.setProperty("value", 0)
        self.download_progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.download_progress_bar.setObjectName("download_progress_bar")

        # 停止下载
        self.end_download_btn = QtWidgets.QPushButton(self.group_box_download)
        self.end_download_btn.setGeometry(QtCore.QRect(1000, 80, 71, 31))
        self.end_download_btn.setObjectName("end_download_btn")
        self.end_download_btn.clicked.connect(self.__stop_download)

        # 编辑组
        self.group_box_editor = QtWidgets.QGroupBox(self.centralwidget)
        self.group_box_editor.setGeometry(QtCore.QRect(20, 260, 1131, 391))
        self.group_box_editor.setObjectName("group_box_editor")
        self.groupBox_4 = QtWidgets.QGroupBox(self.group_box_editor)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 30, 1111, 61))
        self.groupBox_4.setObjectName("groupBox_4")

        # 背景图
        self.select_background_pic_btn = QtWidgets.QPushButton(self.groupBox_4)
        self.select_background_pic_btn.setGeometry(QtCore.QRect(10, 20, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_background_pic_btn.sizePolicy().hasHeightForWidth())
        self.select_background_pic_btn.setSizePolicy(sizePolicy)
        self.select_background_pic_btn.setObjectName("select_background_pic_btn")
        self.select_background_pic_btn.clicked.connect(lambda: self.__select_file("editor", "background_pic"))
        self.background_pic_path_display = QtWidgets.QTextBrowser(self.groupBox_4)
        self.background_pic_path_display.setGeometry(QtCore.QRect(100, 20, 171, 31))
        self.background_pic_path_display.setObjectName("background_pic_path_display")

        # 背景乐
        self.select_background_music_btn = QtWidgets.QPushButton(self.groupBox_4)
        self.select_background_music_btn.setGeometry(QtCore.QRect(290, 20, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_background_music_btn.sizePolicy().hasHeightForWidth())
        self.select_background_music_btn.setSizePolicy(sizePolicy)
        self.select_background_music_btn.setObjectName("select_background_music_btn")
        self.select_background_music_btn.clicked.connect(lambda: self.__select_file("editor", "background_music"))
        self.background_music_path_display = QtWidgets.QTextBrowser(self.groupBox_4)
        self.background_music_path_display.setGeometry(QtCore.QRect(380, 20, 181, 31))
        self.background_music_path_display.setObjectName("background_music_path_display")

        # 水印
        self.select_water_logo_btn = QtWidgets.QPushButton(self.groupBox_4)
        self.select_water_logo_btn.setGeometry(QtCore.QRect(740, 20, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_water_logo_btn.sizePolicy().hasHeightForWidth())
        self.select_water_logo_btn.setSizePolicy(sizePolicy)
        self.select_water_logo_btn.setObjectName("select_water_logo_btn")
        self.select_water_logo_btn.clicked.connect(lambda: self.__select_file("editor", "water_logo"))
        self.water_logo_display = QtWidgets.QTextBrowser(self.groupBox_4)
        self.water_logo_display.setGeometry(QtCore.QRect(830, 20, 231, 31))
        self.water_logo_display.setObjectName("water_logo_display")

        # 音量
        self.label_volume = QtWidgets.QLabel(self.groupBox_4)
        self.label_volume.setGeometry(QtCore.QRect(569, 28, 36, 16))
        self.label_volume.setObjectName("label_volume")
        self.input_volume = QtWidgets.QLineEdit(self.groupBox_4)
        self.input_volume.setGeometry(QtCore.QRect(611, 28, 31, 20))
        self.input_volume.setObjectName("input_volume")
        self.input_volume.editingFinished.connect(
            lambda: self.__line_edit_change("editor", "volume", self.input_volume.text()))

        self.is_music_covered = QtWidgets.QCheckBox(self.groupBox_4)
        self.is_music_covered.setGeometry(QtCore.QRect(650, 30, 71, 16))
        self.is_music_covered.setObjectName("is_music_covered")
        self.is_music_covered.clicked.connect(self.__cover_music)

        # 单个编辑组
        self.groupBox_5 = QtWidgets.QGroupBox(self.group_box_editor)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 100, 561, 281))
        self.groupBox_5.setObjectName("groupBox_5")

        # 源文件目录
        self.select_single_source_path_btn = QtWidgets.QPushButton(self.groupBox_5)
        self.select_single_source_path_btn.setGeometry(QtCore.QRect(20, 60, 75, 31))
        self.select_single_source_path_btn.setObjectName("select_single_source_path_btn")
        self.select_single_source_path_btn.clicked.connect(
            lambda: self.__select_source_path("editor", "single_source_path"))

        # 保存目录
        self.select_save_path_single_btn = QtWidgets.QPushButton(self.groupBox_5)
        self.select_save_path_single_btn.setGeometry(QtCore.QRect(20, 240, 75, 31))
        self.select_save_path_single_btn.setObjectName("select_save_path_single_btn")
        self.select_save_path_single_btn.clicked.connect(lambda: self.__select_save_path("editor", "single_save_path"))

        # 开始剪辑
        self.run_single_btn = QtWidgets.QPushButton(self.groupBox_5)
        self.run_single_btn.setGeometry(QtCore.QRect(370, 240, 141, 31))
        self.run_single_btn.setObjectName("run_single_btn")
        self.run_single_btn.clicked.connect(self.__run_single_editor)

        # 要处理的文件展示
        self.single_video_list = QtWidgets.QListWidget(self.groupBox_5)
        self.single_video_list.setGeometry(QtCore.QRect(20, 110, 491, 121))
        self.single_video_list.setObjectName("single_video_list")

        # 添加单个视频
        self.add_single_btn = QtWidgets.QPushButton(self.groupBox_5)
        self.add_single_btn.setGeometry(QtCore.QRect(510, 110, 31, 23))
        self.add_single_btn.setObjectName("add_single_btn")
        self.add_single_btn.clicked.connect(self.__single_add_row)

        # 删除所选视频
        self.delete_single_btn = QtWidgets.QPushButton(self.groupBox_5)
        self.delete_single_btn.setGeometry(QtCore.QRect(510, 140, 31, 23))
        self.delete_single_btn.setObjectName("delete_single_btn")
        self.delete_single_btn.clicked.connect(self.__single_remove_row)

        # 选择的视频数量
        self.label_video_count = QtWidgets.QLabel(self.groupBox_5)
        self.label_video_count.setGeometry(QtCore.QRect(380, 70, 54, 12))
        self.label_video_count.setObjectName("label_video_count")

        # 展示源目录
        self.editor_single_source_path_display = QtWidgets.QTextBrowser(self.groupBox_5)
        self.editor_single_source_path_display.setGeometry(QtCore.QRect(100, 60, 256, 31))
        self.editor_single_source_path_display.setObjectName("editor_single_source_path_display")

        # 展示保存目录
        self.editor_single_save_path_display = QtWidgets.QTextBrowser(self.groupBox_5)
        self.editor_single_save_path_display.setGeometry(QtCore.QRect(110, 240, 241, 31))
        self.editor_single_save_path_display.setObjectName("editor_single_save_path_display")

        # 展示视频数量
        self.video_count_display = QtWidgets.QTextBrowser(self.groupBox_5)
        self.video_count_display.setGeometry(QtCore.QRect(430, 60, 81, 31))
        self.video_count_display.setObjectName("video_count_display")

        self.label_end = QtWidgets.QLabel(self.groupBox_5)
        self.label_end.setGeometry(QtCore.QRect(100, 30, 41, 21))
        self.label_end.setObjectName("label_end")

        self.label_end_x = QtWidgets.QLabel(self.groupBox_5)
        self.label_end_x.setGeometry(QtCore.QRect(350, 31, 41, 21))
        self.label_end_x.setObjectName("label_end_x")
        self.input_end_x = QtWidgets.QLineEdit(self.groupBox_5)
        self.input_end_x.setGeometry(QtCore.QRect(397, 31, 31, 20))
        self.input_end_x.setObjectName("input_end_x")
        self.input_end_y = QtWidgets.QLineEdit(self.groupBox_5)
        self.input_end_y.setGeometry(QtCore.QRect(487, 31, 31, 20))
        self.input_end_y.setObjectName("input_end_y")
        self.label_end_y = QtWidgets.QLabel(self.groupBox_5)
        self.label_end_y.setGeometry(QtCore.QRect(440, 31, 41, 21))
        self.label_end_y.setObjectName("label_end_y")
        self.input_start_y = QtWidgets.QLineEdit(self.groupBox_5)
        self.input_start_y.setGeometry(QtCore.QRect(307, 31, 31, 20))
        self.input_start_y.setObjectName("input_start_y")
        self.label_start_y = QtWidgets.QLabel(self.groupBox_5)
        self.label_start_y.setGeometry(QtCore.QRect(270, 31, 41, 21))
        self.label_start_y.setObjectName("label_start_y")
        self.label_start_x = QtWidgets.QLabel(self.groupBox_5)
        self.label_start_x.setGeometry(QtCore.QRect(179, 30, 41, 21))
        self.label_start_x.setObjectName("label_start_x")
        self.input_start_x = QtWidgets.QLineEdit(self.groupBox_5)
        self.input_start_x.setGeometry(QtCore.QRect(220, 31, 31, 20))
        self.input_start_x.setObjectName("input_start_x")
        self.input_end_second = QtWidgets.QLineEdit(self.groupBox_5)
        self.input_end_second.setGeometry(QtCore.QRect(140, 30, 31, 20))
        self.input_end_second.setObjectName("input_end_second")
        self.input_front_second = QtWidgets.QLineEdit(self.groupBox_5)
        self.input_front_second.setGeometry(QtCore.QRect(60, 32, 31, 20))
        self.input_front_second.setObjectName("input_front_second")
        self.label_front = QtWidgets.QLabel(self.groupBox_5)
        self.label_front.setGeometry(QtCore.QRect(22, 32, 31, 21))
        self.label_front.setObjectName("label_front")
        self.groupBox_6 = QtWidgets.QGroupBox(self.group_box_editor)
        self.groupBox_6.setGeometry(QtCore.QRect(580, 100, 541, 281))
        self.groupBox_6.setObjectName("groupBox_6")
        self.normal_merge_btn = QtWidgets.QRadioButton(self.groupBox_6)
        self.normal_merge_btn.setGeometry(QtCore.QRect(100, 30, 89, 21))
        self.normal_merge_btn.setObjectName("normal_merge_btn")
        self.label_merge_videos = QtWidgets.QLabel(self.groupBox_6)
        self.label_merge_videos.setGeometry(QtCore.QRect(10, 30, 54, 21))
        self.label_merge_videos.setObjectName("label_merge_videos")
        self.top10_merge_btn = QtWidgets.QRadioButton(self.groupBox_6)
        self.top10_merge_btn.setGeometry(QtCore.QRect(210, 30, 71, 21))
        self.top10_merge_btn.setObjectName("top10_merge_btn")
        self.select_merge_save_path_btn = QtWidgets.QPushButton(self.groupBox_6)
        self.select_merge_save_path_btn.setGeometry(QtCore.QRect(10, 60, 75, 31))
        self.select_merge_save_path_btn.setObjectName("select_merge_save_path_btn")
        self.label_total_duration = QtWidgets.QLabel(self.groupBox_6)
        self.label_total_duration.setGeometry(QtCore.QRect(360, 61, 54, 31))
        self.label_total_duration.setObjectName("label_total_duration")
        self.select_save_path_merge_btn = QtWidgets.QPushButton(self.groupBox_6)
        self.select_save_path_merge_btn.setGeometry(QtCore.QRect(10, 240, 75, 31))
        self.select_save_path_merge_btn.setObjectName("select_save_path_merge_btn")
        self.run_merge_btn = QtWidgets.QPushButton(self.groupBox_6)
        self.run_merge_btn.setGeometry(QtCore.QRect(360, 240, 141, 31))
        self.run_merge_btn.setObjectName("run_merge_btn")
        self.delete_video_to_merge_btn = QtWidgets.QPushButton(self.groupBox_6)
        self.delete_video_to_merge_btn.setGeometry(QtCore.QRect(500, 140, 31, 23))
        self.delete_video_to_merge_btn.setObjectName("delete_video_to_merge_btn")
        self.add_video_to_merge_btn = QtWidgets.QPushButton(self.groupBox_6)
        self.add_video_to_merge_btn.setGeometry(QtCore.QRect(500, 110, 31, 23))
        self.add_video_to_merge_btn.setObjectName("add_video_to_merge_btn")
        self.merge_video_list = QtWidgets.QListWidget(self.groupBox_6)
        self.merge_video_list.setGeometry(QtCore.QRect(10, 111, 491, 121))
        self.merge_video_list.setObjectName("merge_video_list")
        self.merge_save_path_display = QtWidgets.QTextBrowser(self.groupBox_6)
        self.merge_save_path_display.setGeometry(QtCore.QRect(100, 60, 231, 31))
        self.merge_save_path_display.setObjectName("merge_save_path_display")
        self.video_duration_display = QtWidgets.QTextBrowser(self.groupBox_6)
        self.video_duration_display.setGeometry(QtCore.QRect(410, 60, 81, 31))
        self.video_duration_display.setObjectName("video_duration_display")
        self.editor_merge_save_display = QtWidgets.QTextBrowser(self.groupBox_6)
        self.editor_merge_save_display.setGeometry(QtCore.QRect(100, 240, 231, 31))
        self.editor_merge_save_display.setObjectName("editor_merge_save_display")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 1121, 61))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1167, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.group_box_upload.setTitle(_translate("MainWindow", "账号和上传管理"))
        item = self.account_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "account"))
        item = self.account_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "web"))
        item = self.account_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "title"))
        item = self.account_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "caption"))
        item = self.account_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "desc"))
        item = self.account_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "tag"))
        item = self.account_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "视频目录"))
        item = self.account_table.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "视频类型"))
        item = self.account_table.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "默认标题"))
        self.add_account_btn.setText(_translate("MainWindow", "+"))
        self.delete_account_btn.setText(_translate("MainWindow", "-"))
        self.group_box_download.setTitle(_translate("MainWindow", "视频下载"))
        self.pick_web.setItemText(0, _translate("MainWindow", "douyin"))
        self.pick_web.setItemText(1, _translate("MainWindow", "Youtube"))
        self.label_web.setText(_translate("MainWindow", "视频网站："))
        self.label_url.setText(_translate("MainWindow", "主页链接："))
        self.label_save_path_download.setText(_translate("MainWindow", "保存目录："))
        self.is_english_title.setText(_translate("MainWindow", "英文标题"))
        self.web_confirm_btn.setText(_translate("MainWindow", "确认选择"))
        self.download_save_btn.setText(_translate("MainWindow", "路径选择"))
        self.download_btn.setText(_translate("MainWindow", "开始下载"))
        self.end_download_btn.setText(_translate("MainWindow", "结束下载"))
        self.group_box_editor.setTitle(_translate("MainWindow", "视频编辑"))
        self.groupBox_4.setTitle(_translate("MainWindow", "常规设置"))
        self.select_background_pic_btn.setText(_translate("MainWindow", "背景图"))
        self.select_background_music_btn.setText(_translate("MainWindow", "背景乐"))
        self.select_water_logo_btn.setText(_translate("MainWindow", "水印"))
        self.label_volume.setText(_translate("MainWindow", "音量："))
        self.input_volume.setText(_translate("MainWindow", "50"))
        self.is_music_covered.setText(_translate("MainWindow", "是否覆盖"))
        self.groupBox_5.setTitle(_translate("MainWindow", "单视频编辑"))
        self.select_single_source_path_btn.setText(_translate("MainWindow", "原视频目录"))
        self.select_save_path_single_btn.setText(_translate("MainWindow", "保存目录"))
        self.run_single_btn.setText(_translate("MainWindow", "开始剪辑"))
        self.add_single_btn.setText(_translate("MainWindow", "+"))
        self.delete_single_btn.setText(_translate("MainWindow", "-"))
        self.label_video_count.setText(_translate("MainWindow", "总数量："))
        self.label_end.setText(_translate("MainWindow", "片尾"))
        self.label_end_x.setText(_translate("MainWindow", "终点x"))
        self.label_end_y.setText(_translate("MainWindow", "终点y"))
        self.label_start_y.setText(_translate("MainWindow", "起点y"))
        self.label_start_x.setText(_translate("MainWindow", "起点x"))
        self.input_end_second.setText(_translate("MainWindow", "0"))
        self.input_front_second.setText(_translate("MainWindow", "0"))
        self.label_front.setText(_translate("MainWindow", "片头"))
        self.groupBox_6.setTitle(_translate("MainWindow", "合集"))
        self.normal_merge_btn.setText(_translate("MainWindow", "常规合集"))
        self.label_merge_videos.setText(_translate("MainWindow", "合集类型"))
        self.top10_merge_btn.setText(_translate("MainWindow", "top10"))
        self.select_merge_save_path_btn.setText(_translate("MainWindow", "原视频目录"))
        self.label_total_duration.setText(_translate("MainWindow", "总时长："))
        self.select_save_path_merge_btn.setText(_translate("MainWindow", "保存目录"))
        self.run_merge_btn.setText(_translate("MainWindow", "开始剪辑"))
        self.delete_video_to_merge_btn.setText(_translate("MainWindow", "-"))
        self.add_video_to_merge_btn.setText(_translate("MainWindow", "+"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:36pt; color:#00aa00;\">欢迎使用搬运工</span></p></body></html>"))

    def __line_edit_change(self, module, key, val):
        if module == "download":
            self.download_params[key] = val
        elif module == "editor":
            self.editor_parmas[key] = val
        elif module == "upload":
            self.upload_parmas[key] = val

    def __select_save_path(self, module, key):
        save_path = QFileDialog.getExistingDirectory(self.centralwidget, "选择保存路径", "E:/")
        if module == "download":
            self.download_params[key] = save_path
            self.download_save_display.setText(save_path)
        elif module == "editor":
            self.editor_parmas[key] = save_path
            if key == "single_save_path":
                self.editor_single_save_path_display.setText(save_path)
            elif key == "merge_save_path":
                pass
        elif module == "upload":
            self.upload_parmas[key] = save_path

    def __select_source_path(self, module, key):
        file_path = QFileDialog.getExistingDirectory(self.centralwidget, "选择源路径", "E:/")
        if file_path == '':
            return

        if module == "download":
            pass
        elif module == "editor":
            all_files = os.listdir(file_path)
            files = [file for file in all_files if "mp4" in file]
            if key == "single_source_path":
                # 将加载到的文件列表进行展示
                self.single_video_list.clear()
                self.video_count_display.update()
                self.editor_parmas["single_ready_videos"] = [file_path + "/" + file for file in files]
                for i in range(len(files)):
                    item = QListWidgetItem()
                    item.setText(
                        f"%4d | %s" % (i, files[i]))
                    item.setWhatsThis(str(i))
                    self.single_video_list.addItem(item)

                # 总数量
                self.video_count_display.setText(str(len(files)))
                self.video_count_display.setStyleSheet("color:red;font-size:24px")
                self.video_count_display.update()
                self.editor_single_source_path_display.setText(file_path)
            elif key == "merge_source_path":
                pass

        elif module == "upload":
            pass

    def __select_file(self, module, key):
        file, fileType = QFileDialog.getOpenFileName(self.centralwidget, "选择源文件", "E:/")

        if module == "download":
            self.download_params[key] = file

        elif module == "editor":
            self.editor_parmas[key] = file
            if key == "background_pic":
                self.background_pic_path_display.setText(file)
            elif key == "background_music":
                self.background_music_path_display.setText(file)
            elif key == "water_logo":
                self.water_logo_display.setText(file)

        elif module == "upload":
            self.upload_parmas[key] = file

    def __download_thread(self):
        web = self.download_params["web"]
        home_page_url = self.download_params["home_page_url"]
        save_path = self.download_params["save_path"]
        translate_to_english = self.download_params["translate_to_english"]
        self.download_thread = DownloadThread(web, home_page_url, save_path, translate_to_english)
        self.download_thread._signal.connect(self.__print_backlog)
        self.download_thread.start()

        self.download_btn.setEnabled(False)
        self.download_thread.finished.connect(self.__reset_download_params)

    def __print_backlog(self, msg):
        self.download_progress_bar.setValue(int(msg))  # 将线程的参数传入进度条

    def __translate_to_english(self):
        if self.is_english_title.isChecked():
            self.download_params["translate_to_english"] = True
        else:
            self.download_params["translate_to_english"] = False

    def __confirm_web(self):
        self.download_params["web"] = self.pick_web.currentText()
        print(self.download_params)

    def __reset_download_params(self):
        for key in Params.download_keys:
            self.download_params[key] = None

        # ui 还原
        self.download_progress_bar.setValue(0)
        self.download_save_display.setText("")
        self.input_home_url.setText("")
        self.is_english_title.setChecked(False)
        self.download_btn.setEnabled(True)

    def __stop_download(self):
        self.download_thread.terminate()
        self.__reset_download_params()

    def __cover_music(self):
        if self.is_music_covered.isChecked():
            self.editor_parmas["is_music_covered"] = True
        else:
            self.editor_parmas["is_music_covered"] = False

    def __show_list(self, show_items):
        metric, names = show_items[0], show_items[1]
        print(metric)

    def __single_add_row(self):
        # 打开文件
        video, fileType = QFileDialog.getOpenFileName(self.centralwidget, "添加文件", "E:/")
        if video == "":
            return

        # 在列表后添加这个新加的视频
        if self.editor_parmas["single_ready_videos"] is None:
            self.editor_parmas["single_ready_videos"] = []

        self.editor_parmas["single_ready_videos"].append(video)

        # 添加 index | 时长 |名字
        item = QListWidgetItem()
        item.setText(
            f"%4d | %s" % (len(self.single_video_list), video.split("/")[-1]))
        item.setWhatsThis(str(len(self.single_video_list)))
        self.single_video_list.addItem(item)

        self.video_count_display.setText(str(len(self.single_video_list)))
        self.video_count_display.setStyleSheet("color:red;font-size:24px")
        self.video_count_display.update()

    def __single_remove_row(self):
        item = self.single_video_list.currentItem()

        # 没选中任何要删除的
        if item is None:
            return

        # 正常删除
        index = item.whatsThis()
        self.single_video_list.takeItem(self.single_video_list.row(item))
        # 把下标存起来
        if self.editor_parmas["single_del_videos"] is None:
            self.editor_parmas["single_del_videos"] = []
        self.editor_parmas["single_del_videos"].append(str(index))
        # 更新总时长
        self.video_count_display.setText(str(len(self.editor_parmas["single_ready_videos"]) - len(self.editor_parmas["single_del_videos"])))
        self.video_count_display.setStyleSheet("color:red;font-size:24px")
        self.video_count_display.update()

        # 若已经都没有了，则重置源目录相关的参数
        if len(self.single_video_list) == 0:
            self.editor_parmas["single_del_videos"] = None
            self.editor_parmas["single_ready_videos"] = None
            self.single_video_list.clear()
            self.video_count_display.setText("")
            self.editor_single_source_path_display.setText("")

            return

    def __reset_single_params(self):

        for key in Params.single_editor_keys:
            self.editor_parmas[key] = None

        self.single_video_list.clear()
        self.video_count_display.setText("")
        self.editor_single_source_path_display.setText("")
        self.run_single_btn.setEnabled(True)

    def __run_single_editor(self):
        single_ready_videos = []
        if self.editor_parmas["single_del_videos"] is None:
            single_ready_videos = self.editor_parmas["single_ready_videos"]
        else:
            for idx in range(len(self.editor_parmas["single_ready_videos"])):
                if idx not in self.editor_parmas["single_del_videos"]:
                    single_ready_videos.append(self.editor_parmas["single_ready_videos"][idx])

        background_pic = self.editor_parmas["background_pic"]
        background_audio = self.editor_parmas["background_music"]
        volume = self.editor_parmas["volume"]
        original_autio_off = self.editor_parmas["is_music_covered"]
        water_logo = self.editor_parmas["water_logo"]
        output_path = self.editor_parmas["single_save_path"]

        self.single_editor_thread = EditorThread("single", single_ready_videos, background_pic, background_audio, volume,
                                                 original_autio_off, water_logo, output_path, self.editor_parmas)

        # list展示
        self.single_editor_thread._signal.connect(self.__show_list)
        self.single_editor_thread.start()
        self.run_single_btn.setEnabled(False)
        self.single_editor_thread.finished.connect(self.__reset_single_params)