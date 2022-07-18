from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
from ui.add_account import Ui_Dialog

from Params import Params

import json
import os


class AccountDialog(QDialog, Ui_Dialog):
    _end_signal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(AccountDialog, self).__init__(parent)
        self.setupUi(self)
        self.accounts = self.__load_local_accounts()
        self.finished_btn.clicked.connect(self.__finished)

    def __load_local_accounts(self):
        '''
        加载本地的账号文件
        :return:
        '''
        account_path = os.path.abspath(os.path.join(os.getcwd(),  "resource", "account_conf.json"))
        if not os.path.exists(account_path):
            return dict()

        with open(account_path, mode="r", encoding='utf-8') as meta_json:
            # 在table中进行展示
            meta_dict = json.load(meta_json)

            return meta_dict

    def __finished(self):
        '''
        添加账号完毕，参数传回主页面，进行更新和保存
        :return:
        '''
        res = dict()
        res["account"] = self.account.text()
        res["web"] = self.web.currentText()
        res["title"] = self.title.text()
        res["caption"] = self.caption.text()
        res["description"] = self.description.text()
        res["tags"] = self.tags.text()
        res["title_tags"] = self.title_tags.text()
        res["video_path"] = self.video_path.text()
        res["video_type"] = self.type.currentText()
        res["use_file_title"] = self.user_file_title.currentText()

        success = True
        # 没有account
        if "account" not in res.keys() or "web" not in res.keys() or res["account"] == "":
            QMessageBox.warning(self, "提示", "需要填写账号&web", QMessageBox.Yes)
            success = False
        elif any(char in res['account'] and char for char in Params.file_name_black_char):
            QMessageBox.warning(self, "提示", "账号名中不要包含特殊字符*|等", QMessageBox.Yes)
            success = False
        elif len(res["title_tags"]) > 50:
            QMessageBox.warning(self, "提示", "youtube标题tags长度超过50")
            success = False
        elif (len(res["title"]) + len(res["title_tags"]) ) > 100:
            QMessageBox.warning(self, "提示", "youtube标题长度超过100, 标题：%d, 标题tags：%d" % (len(res["title"]), len(res["title_tags"])))
            success = False
        elif len(res["description"]) > 5000:
            QMessageBox.warning(self, "提示", "youtube描述长度超过5000")
            success = False
        elif len(res["tags"]) > 500:
            QMessageBox.warning(self, "提示", "youtube的tags长度超过5000")
            success = False
        else:
            # 不希望被覆盖
            if res["account"] in self.accounts.keys():
                is_covered = QMessageBox.warning(self, "提示", "该账号已存在，是否覆盖", QMessageBox.No | QMessageBox.Yes)
                if is_covered == QMessageBox.No:
                    success = False

        if success:
            self._end_signal.emit(res)
            self.close()
