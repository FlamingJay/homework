import re
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QMessageBox, QTableWidgetItem, \
    QProgressDialog
from moviepy.video.io.VideoFileClip import VideoFileClip

from download.DownloadThread import DownloadThread
from download.TranslateThread import TranslateThread
from editor.EditorThread import EditorThread
from ui.LoadingDialog import LoadingDialog
from ui.double_page import Ui_MainWindow

from Params import *
import json
import sys
import os

from ui.AccountDialog import AccountDialog
from ui.TextCellDialog import TableCellDialog
from ui.ComboxDialog import ComboxDialog

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

        # 进行展示当前账号
        self.upload_parmas["accounts"] = self.__load_local_accounts()
        self.account_table.doubleClicked.connect(self.__change_cell)

        # 小工具
        self.tool_params = dict()

    def __init_btn_click(self):
        '''
        对btn的信号槽进行关联
        :return:
        '''
        # ------------- 下载相关  ----------------------
        # 确认网址
        self.web_confirm_btn.clicked.connect(self.__confirm_web)
        self.input_home_url.editingFinished.connect(
            lambda: self.__line_edit_change("download", "home_page_url", self.input_home_url.text()))
        self.download_save_btn.clicked.connect(lambda: self.__select_save_path("download", "save_path"))
        self.download_btn.clicked.connect(self.__download_thread)
        self.end_download_btn.clicked.connect(self.__stop_download)

        # ------------- 视频剪辑公共部分  ----------------
        self.select_background_pic_btn.clicked.connect(lambda: self.__select_file("editor", "background_pic"))
        self.input_background_pic_rate.editingFinished.connect(
            lambda: self.__line_edit_change("editor", "background_pic_rate", self.input_background_pic_rate.text()))
        self.select_background_music_btn.clicked.connect(lambda: self.__select_file("editor", "background_music"))
        self.select_water_logo_btn.clicked.connect(lambda: self.__select_file("editor", "water_logo"))
        self.is_music_covered.clicked.connect(self.__cover_music)

        # ------------- 单视频剪辑相关  -----------------
        self.select_single_source_path_btn.clicked.connect(
            lambda: self.__select_source_path("editor", "single_source_path"))

        self.input_start_x.editingFinished.connect(
            lambda: self.__line_edit_change("editor", "input_start_x", self.input_start_x.text()))
        self.input_start_y.editingFinished.connect(
            lambda: self.__line_edit_change("editor", "input_start_y", self.input_start_y.text()))
        self.input_end_x.editingFinished.connect(
            lambda: self.__line_edit_change("editor", "input_end_x", self.input_end_x.text()))
        self.input_end_y.editingFinished.connect(
            lambda: self.__line_edit_change("editor", "input_end_y", self.input_end_y.text()))
        self.input_front_second.editingFinished.connect(
            lambda: self.__line_edit_change("editor", "front_cut_dur", self.input_front_second.text()))
        self.input_end_second.editingFinished.connect(
            lambda: self.__line_edit_change("editor", "end_cut_dur", self.input_end_second.text()))

        self.select_save_path_single_btn.clicked.connect(lambda: self.__select_save_path("editor", "single_save_path"))
        self.run_single_btn.clicked.connect(self.__run_single_editor)
        self.add_single_btn.clicked.connect(self.__single_add_row)
        self.delete_single_btn.clicked.connect(self.__single_remove_row)

        # ------------- 合集剪辑相关  -----------------
        self.merge_type_btn_group.buttonClicked.connect(self.__select_merge_type)
        self.merge_type_btn_group.addButton(self.normal_merge_btn, 11)
        self.merge_type_btn_group.addButton(self.top10_merge_btn, 12)
        self.merge_type_btn_group.setExclusive(True)
        self.select_merge_source_path_btn.clicked.connect(lambda: self.__select_multi_files("editor", "merge_source_path"))
        self.add_merge_btn.clicked.connect(self.__merge_add_row)
        self.delete_merge_btn.clicked.connect(self.__merge_remove_row)
        self.select_save_path_merge_btn.clicked.connect(lambda: self.__select_save_path("editor", "merge_save_path"))
        self.run_merge_btn.clicked.connect(self.__run_merge_editor)

        # ------------- 账号管理相关  -----------------
        self.add_account_btn.clicked.connect(self.__account_add_row)
        self.delete_account_btn.clicked.connect(self.__account_remove_row)

        # ------------- 其他小工具  -----------------
        self.select_translate_dir_btn.clicked.connect(lambda: self.__select_source_path("tool", "translate_path"))
        self.run_translate_btn.clicked.connect(self.__run_translate)

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
        elif module == "tool":
            self.translate_path.setText(file_path)

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


        self.download_thread = DownloadThread(web, home_page_url, save_path)
        self.download_thread._download_signal.connect(self.__print_backlog)
        self.download_thread.start()

        self.download_btn.setEnabled(False)
        self.download_thread.finished.connect(self.__reset_download_params)

    def __print_backlog(self, msg):
        '''
        多线程下载进度条
        :param msg:
        :return:
        '''
        if msg == -1:
            self.loading_dialog = LoadingDialog("loading")
        elif msg == -2:
            self.loading_dialog.close()
        else:
            self.download_progress_bar.setValue(int(msg))  # 将线程的参数传入进度条

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
        self.single_video_list.takeItem(self.single_video_list.row(item))

        # 更新总时长
        self.video_count_display.setText(
            str(len(self.single_video_list)))
        self.video_count_display.setStyleSheet("color:red;font-size:24px")
        self.video_count_display.update()

        # 若已经都没有了，则重置源目录相关的参数
        if len(self.single_video_list) == 0:
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
        self.single_editor_dialog.close()
        QMessageBox.information(self.centralwidget, "恭喜你", "剪辑完成")
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
        index_list = []
        for i in range(len(self.single_video_list)):
            index_list.append(int(self.single_video_list.item(i).whatsThis()))

        single_ready_videos = [self.editor_parmas["merge_ready_videos"][index] for index in index_list]

        background_pic = self.editor_parmas["background_pic"]
        background_pic_rate = self.editor_parmas["background_pic_rate"]
        background_audio = self.editor_parmas["background_music"]
        volume = self.editor_parmas["volume"]
        original_autio_off = self.editor_parmas["is_music_covered"]
        water_logo = self.editor_parmas["water_logo"]
        output_path = self.editor_parmas["single_save_path"]
        self.single_editor_dialog = LoadingDialog("single_editor")

        self.single_editor_thread = EditorThread("single", single_ready_videos, background_pic, background_pic_rate,
                                                 background_audio, volume, original_autio_off,
                                                 water_logo, output_path, self.editor_parmas)

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
        index = len(self.editor_parmas["merge_ready_videos"]) - 1
        item.setText(f"%4d | %4d秒 | %s" % (index, duration, video.split("/")[-1]))
        item.setWhatsThis(str(index))
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

        # 更新总时长
        self.editor_parmas["total_duration"] -= self.editor_parmas["merge_video_duration"][int(index)]
        self.video_duration_display.setText(
            str(self.editor_parmas["total_duration"]))
        self.video_duration_display.setStyleSheet("color:red;font-size:24px")
        self.video_duration_display.update()

        # 若已经都没有了，则重置源目录相关的参数
        if len(self.merge_video_list) == 0:
            self.editor_parmas["merge_ready_videos"] = None
            self.editor_parmas["total_duration"] = 0
            self.editor_parmas["merge_video_duration"] = None
            self.merge_video_list.clear()
            self.video_duration_display.setText("")
            self.editor_merge_source_path_display.setText("")

            return

    def __select_merge_type(self):
        '''
        选择合集类型
        :return:
        '''
        sender = self.sender()
        if sender == self.merge_type_btn_group:
            if self.merge_type_btn_group.checkedId() == 11:
                self.editor_parmas["merge_type"] = 'normal'
                self.top_10_status.setText("")
            elif self.merge_type_btn_group.checkedId() == 12:
                self.editor_parmas["merge_type"] = 'top10'
                # 读取top10转场
                top10_path = QFileDialog.getExistingDirectory(self, "选取top10目录", "E:/")
                if top10_path == "":
                    self.top10_merge_btn.setChecked(False)
                    self.editor_parmas["merge_type"] = None
                    self.top_10_status.setText("未选中任何目录")
                    return

                files = os.listdir(top10_path)
                files = [file for file in files if ".mp4" in file]
                if len(files) != 12:
                    # todo: 数量提示：top10 + 开场 + 结尾
                    QMessageBox.critical(self.centralwidget, "错误", "top10转场素材不是12个(top10 + 开场 + 结尾)")
                    return
                files.sort(reverse=True)
                self.editor_parmas["merge_top10_path"] = []
                for file in files:
                    self.editor_parmas["merge_top10_path"].append(top10_path + "/" + file)
                self.top_10_status.setText(top10_path)
            else:
                self.editor_parmas["merge_type"] = 'normal'
                self.top_10_status.setText("")

    def __reset_merge_params(self):
        '''
        重置合集相关参数
        :return:
        '''
        self.merge_editor_dialog.close()

        QMessageBox.information(self.centralwidget, "恭喜你", "剪辑完成")
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
        index_list = []
        for i in range(len(self.merge_video_list)):
            index_list.append(int(self.merge_video_list.item(i).whatsThis()))

        merge_ready_videos = [self.editor_parmas["merge_ready_videos"][index] for index in index_list]
        final_merge_videos = []

        if self.editor_parmas["merge_type"] == "top10":
            if len(self.editor_parmas["merge_ready_videos"]) < 10:
                # todo: 提示数量小于10
                QMessageBox.critical(self.centralwidget, "错误", "视频数不足10个")
                return
            elif len(self.editor_parmas["merge_ready_videos"]) > 10:
                # todo: 提示数量大于10
                QMessageBox.critical(self.centralwidget, "错误", "视频数超过10个")
                return
            else:
                final_merge_videos.append(self.editor_parmas["merge_top10_path"][-2])
                for i in range(len(self.editor_parmas["merge_ready_videos"])):
                    final_merge_videos.append(self.editor_parmas["merge_top10_path"][i])
                    final_merge_videos.append(self.editor_parmas["merge_ready_videos"][i])
                final_merge_videos.append(self.editor_parmas["merge_top10_path"][-1])
        else:
            final_merge_videos = merge_ready_videos

        background_pic = self.editor_parmas["background_pic"]
        background_pic_rate = self.editor_parmas["background_pic_rate"]
        background_audio = self.editor_parmas["background_music"]
        volume = self.editor_parmas["volume"]
        original_autio_off = self.editor_parmas["is_music_covered"]
        water_logo = self.editor_parmas["water_logo"]
        output_path = self.editor_parmas["merge_save_path"]

        self.merge_editor_dialog = LoadingDialog("merge_editor")

        self.merge_editor_thread = EditorThread("merge", final_merge_videos, background_pic, background_pic_rate,
                                                background_audio, volume, original_autio_off,
                                                water_logo, output_path, self.editor_parmas)

        self.merge_editor_thread.start()
        self.run_merge_btn.setEnabled(False)
        self.merge_editor_thread.finished.connect(self.__reset_merge_params)


    def __account_add_row(self):
        '''
        添加一行新的账号
        :return:
        '''
        self.add_dialog = AccountDialog()
        self.add_dialog.show()
        self.add_dialog._end_signal.connect(self.__add_finished)

    def __account_remove_row(self):
        '''
        删掉一行账号
        :return:
        '''
        curRow = self.account_table.currentRow()
        if curRow == -1:
            return

        confirm = QMessageBox.warning(self.centralwidget, "请注意！", "您将要删掉该账号，后台数据也会被删除", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.No:
            return
        account = self.account_table.item(curRow, 0).text()
        web = self.account_table.item(curRow, 1).text()
        video_type = self.account_table.item(curRow, 8).text()
        file = "_".join([web, account, video_type]) + ".bat"

        self.account_table.removeRow(curRow)
        self.upload_parmas["accounts"].pop(account)
        # 更新json
        self.__rewrite_local_accounts_json()
        # 删掉bat文件
        file = os.path.join(os.getcwd(), "resource", file)
        if os.path.exists(file):
            os.remove(file)

    def __load_local_accounts(self):
        '''
        加载本地的账号文件
        :return:
        '''
        if not os.path.exists("resource/account_conf.json"):
            return dict()

        with open("resource/account_conf.json", mode="r", encoding='utf-8') as meta_json:
            meta_dict = json.load(meta_json)
            for account in meta_dict.keys():
                curRowCount = self.account_table.rowCount()
                self.account_table.insertRow(curRowCount)
                for idx, key in enumerate(Params.account_info):


                    if key in meta_dict[account].keys():
                        self.account_table.setItem(curRowCount, idx, QTableWidgetItem(meta_dict[account][key]))
                    else:
                        meta_dict[account][key] = ""
                        self.account_table.setItem(curRowCount, idx, QTableWidgetItem(""))

            return meta_dict

    def __rewrite_local_accounts_json(self):
        '''
        重写账号文件，并生成bat文件
        :return:
        '''
        accounts = self.upload_parmas["accounts"]
        with open("resource/account_conf.json", mode="w", encoding='utf-8') as file:
            json.dump(accounts, file, indent=2)
        # 生成一遍.bat文件
        file = os.getcwd() + os.sep + "upload" + os.sep + "AutoUpload.py"
        root = os.getcwd() + os.sep + "upload"
        for account in accounts.keys():
            file_name = "_".join([accounts[account]["web"], account, accounts[account]["video_type"]])
            content = []
            for key in Params.bat_info:
                if key == "meta":
                    content.append("--" + key + " " + "account_conf.json")
                else:
                    content.append("--" + key + " " + "\"" + accounts[account][key] + "\"")

            content = " ".join([r"python " + file, "--root " + root, " ".join(content)])
            with open("./resource/" + file_name + ".bat", "w", encoding="utf-8") as fwrite:
                fwrite.write(content)

    def __add_finished(self, new_account):
        '''
        信号槽：收到完成账号注册的信息，并将注册信息进行添加，允许覆盖
        :param new_account:
        :return:
        '''
        if "account" not in new_account.keys():
            return

        account = new_account["account"]
        # 判断是否已存在,若存在，则找到对应的行进行覆盖
        if account in self.upload_parmas["accounts"].keys():
            for row in range(self.account_table.rowCount()):
                if self.account_table.item(row, 0).text() == account:
                    curRowCount = row
                    break
        else:
            curRowCount = self.account_table.rowCount()
            self.account_table.insertRow(curRowCount)

        self.upload_parmas["accounts"][account] = dict()
        for idx, key in enumerate(Params.account_info):
            if key not in new_account.keys():
                new_account[key] = ""

            self.upload_parmas["accounts"][account][key] = new_account[key]
            self.account_table.setItem(curRowCount, idx, QTableWidgetItem(new_account[key]))

        self.__rewrite_local_accounts_json()

    def __change_cell(self):
        '''
        单元格修改：区分combox和text的
        :return:
        '''
        item = self.account_table.currentItem().text()
        col = self.account_table.currentColumn()

        if col == 0:
            QMessageBox.critical(self.centralwidget, "错误", "无法修改账号名")
            return
        elif col in [Params.account_info.index("web"), Params.account_info.index("video_type"), Params.account_info.index("use_file_title")]:
            self.combox_dialog = ComboxDialog(Params.account_info[col])
            self.combox_dialog.show()
            self.combox_dialog._combox_cell_signal.connect(self.__table_update)
        else:
            self.cell_dialog = TableCellDialog(item)
            self.cell_dialog.show()
            self.cell_dialog._text_cell_signal.connect(self.__table_update)

    def __table_update(self, content):
        '''
        更新表格内容和后台数据
        :param content:
        :return:
        '''
        row = self.account_table.currentRow()
        col = self.account_table.currentColumn()

        self.account_table.setItem(row, col, QTableWidgetItem(content))

        account = self.account_table.item(row, 0).text()
        self.upload_parmas["accounts"][account][Params.account_info[col]] = content
        self.__rewrite_local_accounts_json()

    def __run_translate(self):
        file_path = self.translate_path.toPlainText()
        self.translate_thread = TranslateThread(file_path)
        self.translate_thread._translate_signal.connect(self.__translate_progress)
        self.translate_thread.start()

        self.run_translate_btn.setEnabled(False)
        self.translate_thread.finished.connect(self.__reset_translate_params)

    def __translate_progress(self, msg):
        self.translate_progress_bar.setValue(msg)

    def __reset_translate_params(self):
        QMessageBox.information(self.centralwidget, "翻译", "亲爱的杜总，翻译完了哈")
        self.translate_progress_bar.setValue(0)
        self.run_translate_btn.setEnabled(True)
        self.translate_path.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())
