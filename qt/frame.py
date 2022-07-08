from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from moviepy.video.io.VideoFileClip import VideoFileClip

from qt.DownloadThread import DownloadThread
from qt.EditorThread import EditorThread
from shortVideo2 import Ui_MainWindow
import sys
from Params import *
import os


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.__init_btn_click()

        # 初始化参数
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

    def __init_btn_click(self):
        '''
        对btn的信号槽进行关联
        :return:
        '''
        # ------------- 下载相关  ----------------------
        # 确认网址
        self.web_confirm_btn.clicked.connect(self.__confirm_web)
        self.is_english_title.clicked.connect(self.__translate_to_english)
        self.download_save_btn.clicked.connect(lambda: self.__select_save_path("download", "save_path"))
        self.download_btn.clicked.connect(self.__download_thread)
        self.end_download_btn.clicked.connect(self.__stop_download)

        # ------------- 视频剪辑公共部分  ----------------
        self.select_background_pic_btn.clicked.connect(lambda: self.__select_file("editor", "background_pic"))
        self.select_background_music_btn.clicked.connect(lambda: self.__select_file("editor", "background_music"))
        self.select_water_logo_btn.clicked.connect(lambda: self.__select_file("editor", "water_logo"))
        self.is_music_covered.clicked.connect(self.__cover_music)

        # ------------- 单视频剪辑相关  -----------------
        self.select_single_source_path_btn.clicked.connect(
            lambda: self.__select_source_path("editor", "single_source_path"))
        self.select_save_path_single_btn.clicked.connect(lambda: self.__select_save_path("editor", "single_save_path"))
        self.run_single_btn.clicked.connect(self.__run_single_editor)
        self.add_single_btn.clicked.connect(self.__single_add_row)
        self.delete_single_btn.clicked.connect(self.__single_remove_row)

        # ------------- 合集剪辑相关  -----------------
        self.merge_type_btn_group.buttonClicked.connect(self.__select_merge_type)
        self.select_merge_source_path_btn.clicked.connect(lambda: self.__select_multi_files("editor", "merge_source_path"))
        self.add_merge_btn.clicked.connect(self.__merge_add_row)
        self.delete_merge_btn.clicked.connect(self.__merge_remove_row)
        self.select_save_path_merge_btn.clicked.connect(lambda: self.__select_save_path("editor", "merge_save_path"))

        self.run_merge_btn.clicked.connect(self.__run_merge_editor)

    def __line_edit_change(self, module, key, val):
        '''
        文本框编辑
        :param module:
        :param key:
        :param val:
        :return:
        '''
        if module == "download":
            self.download_params[key] = val
        elif module == "editor":
            self.editor_parmas[key] = val
        elif module == "upload":
            self.upload_parmas[key] = val

    def __select_save_path(self, module, key):
        '''
        选择保存目录
        :param module:
        :param key:
        :return:
        '''
        save_path = QFileDialog.getExistingDirectory(self.centralwidget, "选择保存路径", "E:/")
        if module == "download":
            self.download_params[key] = save_path
            self.download_save_display.setText(save_path)
        elif module == "editor":
            self.editor_parmas[key] = save_path
            if key == "single_save_path":
                self.editor_single_save_path_display.setText(save_path)
            elif key == "merge_save_path":
                self.editor_merge_save_path_display.setText(save_path)
        elif module == "upload":
            self.upload_parmas[key] = save_path

    def __select_source_path(self, module, key):
        '''
        选择数据源目录
        :param module:
        :param key:
        :return:
        '''
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
                    item.setText(f"%4d | %s" % (i, files[i]))
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
        '''
        选择单个文件
        :param module:
        :param key:
        :return:
        '''
        file, fileType = QFileDialog.getOpenFileName(self.centralwidget, "选择源文件", "E:/")
        if file == '':
            return

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
        '''
        多线程下载
        :return:
        '''
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
        '''
        多线程下载进度条
        :param msg:
        :return:
        '''
        self.download_progress_bar.setValue(int(msg))  # 将线程的参数传入进度条

    def __translate_to_english(self):
        '''
        下载是否翻译成英文
        :return:
        '''
        if self.is_english_title.isChecked():
            self.download_params["translate_to_english"] = True
        else:
            self.download_params["translate_to_english"] = False

    def __confirm_web(self):
        '''
        确认网站
        :return:
        '''
        self.download_params["web"] = self.pick_web.currentText()
        print(self.download_params)

    def __reset_download_params(self):
        '''
        下载功能参数复位
        :return:
        '''
        for key in Params.download_keys:
            self.download_params[key] = None

        # ui 还原
        self.download_progress_bar.setValue(0)
        self.download_save_display.setText("")
        self.input_home_url.setText("")
        self.is_english_title.setChecked(False)
        self.download_btn.setEnabled(True)

    def __stop_download(self):
        '''
        停止下载
        :return:
        '''
        self.download_thread.terminate()
        self.__reset_download_params()

    def __cover_music(self):
        '''
        剪辑公共 - 音频是否覆盖原音频
        :return:
        '''
        if self.is_music_covered.isChecked():
            self.editor_parmas["is_music_covered"] = True
        else:
            self.editor_parmas["is_music_covered"] = False

    def __show_list(self, show_items):
        '''
        todo：看看有什么可以用的
        :param show_items:
        :return:
        '''
        metric, names = show_items[0], show_items[1]
        print(metric)

    def __single_add_row(self):
        '''
        单个要剪辑的视频添加
        :return:
        '''
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
        '''
        单个视频去除
        :return:
        '''
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
        self.video_count_display.setText(
            str(len(self.editor_parmas["single_ready_videos"]) - len(self.editor_parmas["single_del_videos"])))
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
        '''
        单视频剪辑 - 参数复位
        :return:
        '''
        for key in Params.single_editor_keys:
            self.editor_parmas[key] = None

        self.single_video_list.clear()
        self.video_count_display.setText("")
        self.editor_single_source_path_display.setText("")
        self.editor_single_save_path_display.setText("")
        self.run_single_btn.setEnabled(True)

    def __run_single_editor(self):
        '''
        开始进行单视频剪辑
        :return:
        '''
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

        self.single_editor_thread = EditorThread("single", single_ready_videos, background_pic, background_audio,
                                                 volume,
                                                 original_autio_off, water_logo, output_path, self.editor_parmas)

        # list展示
        self.single_editor_thread._signal.connect(self.__show_list)
        self.single_editor_thread.start()
        self.run_single_btn.setEnabled(False)
        self.single_editor_thread.finished.connect(self.__reset_single_params)

    def __select_multi_files(self, module, key):
        '''
        选取多个文件
        :param module:
        :param key:
        :return:
        '''
        files, fileTypes = QFileDialog.getOpenFileNames(self, "选择源文件", r"E:\homeWork\editor\demo")

        if len(files) == 0:
            return

        if module == "download":
            pass
        elif module == "editor":
            if key == "merge_source_path":
                if self.editor_parmas["merge_ready_videos"] is None:
                    self.editor_parmas["merge_ready_videos"] = []
                if self.editor_parmas["merge_video_duration"] is None:
                    self.editor_parmas["merge_video_duration"] = []
                if self.editor_parmas["total_duration"] is None:
                    self.editor_parmas["total_duration"] = 0

                # 将加载到的文件列表进行展示
                for i in range(len(files)):
                    self.editor_parmas["merge_ready_videos"].append(files[i])
                    xx = VideoFileClip(files[i])
                    duration = xx.duration
                    self.editor_parmas["merge_video_duration"].append(duration)
                    self.editor_parmas["total_duration"] += duration
                    # 添加 index | 时长 |名字
                    item = QListWidgetItem()
                    item.setText(f"%4d | %4.2f秒 | %s" % (i, duration, files[i].split("/")[-1]))
                    item.setWhatsThis(str(i))
                    self.merge_video_list.addItem(item)

                self.video_duration_display.setText(str(self.editor_parmas["total_duration"]))
                self.video_duration_display.setStyleSheet("color:red;font-size:24px")
                self.video_duration_display.update()

                self.editor_merge_source_path_display.setText(";".join(files))
        elif module == "upload":
            pass
        else:
            pass

    def __merge_add_row(self):
        '''
        合集视频添加一行
        :return:
        '''
        # 打开文件
        video, fileType = QFileDialog.getOpenFileName(self.centralwidget, "添加文件", "E:/")
        if video == "":
            return

        xx = VideoFileClip(video)
        duration = xx.duration
        del xx

        # 在列表后添加这个新加的视频
        if self.editor_parmas["merge_ready_videos"] is None:
            self.editor_parmas["merge_ready_videos"] = []
        if self.editor_parmas["merge_video_duration"] is None:
            self.editor_parmas["merge_video_duration"] = []
        if self.editor_parmas["total_duration"] is None:
            self.editor_parmas["total_duration"] = 0

        self.editor_parmas["merge_ready_videos"].append(video)
        self.editor_parmas["merge_video_duration"].append(duration)
        self.editor_parmas["total_duration"] += duration

        # 添加 index | 时长 |名字
        item = QListWidgetItem()
        item.setText(f"%4d | %4d秒 | %s" % (len(self.editor_parmas["merge_ready_videos"]), duration, video.split("/")[-1]))
        item.setWhatsThis(str(len(self.editor_parmas["merge_ready_videos"])))
        self.merge_video_list.addItem(item)

        self.video_duration_display.setText(str(self.editor_parmas["total_duration"]))
        self.video_duration_display.setStyleSheet("color:red;font-size:24px")
        self.video_duration_display.update()

    def __merge_remove_row(self):
        '''
        单个视频去除
        :return:
        '''
        item = self.merge_video_list.currentItem()

        # 没选中任何要删除的
        if item is None:
            return

        # 正常删除
        index = item.whatsThis()
        self.merge_video_list.takeItem(self.merge_video_list.row(item))
        # 把下标存起来
        if self.editor_parmas["merge_del_videos"] is None:
            self.editor_parmas["merge_del_videos"] = []
        self.editor_parmas["merge_del_videos"].append(str(index))
        # 更新总时长
        self.editor_parmas["total_duration"] -= self.editor_parmas["merge_video_duration"][int(index)]
        self.video_duration_display.setText(
            str(self.editor_parmas["total_duration"]))
        self.video_duration_display.setStyleSheet("color:red;font-size:24px")
        self.video_duration_display.update()

        # 若已经都没有了，则重置源目录相关的参数
        if len(self.merge_video_list) == 0:
            self.editor_parmas["merge_del_videos"] = None
            self.editor_parmas["merge_ready_videos"] = None
            self.editor_parmas["total_duration"] = 0
            self.editor_parmas["merge_video_duration"] = None
            self.merge_video_list.clear()
            self.video_duration_display.setText("")
            self.editor_merge_source_path_display.setText("")

            return

    def __select_merge_type(self):
        sender = self.sender()
        if sender == self.merge_type_btn_group:
            if self.merge_type_btn_group.checkedId() == 11:
                self.editor_parmas["merge_type"] = 'normal'
            elif self.merge_type_btn_group.checkedId() == 12:
                self.editor_parmas["merge_type"] = 'top10'
                # 读取top10转场
                top10_path = QFileDialog.getExistingDirectory(self, "选取top10目录", "E:/")
                files = os.listdir(top10_path)
                files = [file for file in files if "mp4" in file]
                if len(files) != 12:
                    # todo: 数量提示：top10 + 开场 + 结尾
                    return
                files.sort(reverse=True)
                self.editor_parmas["merge_top10_path"] = []
                for file in files:
                    self.editor_parmas["merge_top10_path"].append(top10_path + "/" + file)
            else:
                self.editor_parmas["merge_type"] = 'normal'

    def __reset_merge_params(self):
        for param in Params.merge_editor_keys:
            self.editor_parmas[param] = None
        self.merge_video_list.clear()
        self.video_duration_display.setText("")
        self.editor_merge_source_path_display.setText("")
        self.editor_merge_save_path_display.setText("")
        self.run_merge_btn.setEnabled(True)

    def __run_merge_editor(self):
        '''
        开始进行合集视频剪辑
        :return:
        '''
        merge_ready_videos = []
        if self.editor_parmas["merge_del_videos"] is None:
            merge_ready_videos = self.editor_parmas["merge_ready_videos"]
        else:
            for idx in range(len(self.editor_parmas["merge_ready_videos"])):
                if idx not in self.editor_parmas["merge_del_videos"]:
                    merge_ready_videos.append(self.editor_parmas["merge_ready_videos"][idx])

        final_merge_videos = []

        if self.editor_parmas["merge_type"] == "top10":
            if len(self.editor_parmas["merge_ready_videos"]) < 10:
                # todo: 提示数量小于10
                return
            elif len(self.editor_parmas["merge_ready_videos"]) > 10:
                # todo: 提示数量大于10
                return
            else:
                final_merge_videos.append(self.editor_parmas["merge_top10_path"][-2])
                for i in range(len(self.editor_parmas["merge_ready_videos"])):
                    final_merge_videos.append(self.editor_parmas["merge_ready_videos"][i])
                    final_merge_videos.append(self.editor_parmas["merge_top10_path"][i])
                final_merge_videos.append(self.editor_parmas["merge_top10_path"][-1])
        else:
            final_merge_videos = merge_ready_videos


        background_pic = self.editor_parmas["background_pic"]
        background_audio = self.editor_parmas["background_music"]
        volume = self.editor_parmas["volume"] if self.editor_parmas["volume"] is not None else self.input_volume.text()
        original_autio_off = self.editor_parmas["is_music_covered"]
        water_logo = self.editor_parmas["water_logo"]
        output_path = self.editor_parmas["merge_save_path"]

        self.merge_editor_thread = EditorThread("merge", final_merge_videos, background_pic, background_audio,
                                                 volume,
                                                 original_autio_off, water_logo, output_path, self.editor_parmas)

        # list展示
        self.merge_editor_thread._signal.connect(self.__show_list)
        self.merge_editor_thread.start()
        self.run_merge_btn.setEnabled(False)
        self.merge_editor_thread.finished.connect(self.__reset_merge_params)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())