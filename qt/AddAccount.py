from PyQt5.QtWidgets import QDialog, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal, QRect

import json
import os


class AddAccount(QDialog):
    _end_signal = pyqtSignal(dict)

    def __init__(self):
        super(AddAccount, self).__init__()
        self.initUI()
        self.accounts = self.__load_local_accounts()

    def initUI(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("子窗口")
        self.resize(280, 280)

        self.btn2 = QPushButton("finished", self)
        self.btn2.setGeometry(QRect(150, 80, 75, 31))
        self.btn2.clicked.connect(self.finished)


    def __load_local_accounts(self):
        if not os.path.exists("./resource/account_conf.json"):
            # todo: 考虑需不需要在这里新建文件
            return dict()

        with open("./resource/account_conf.json", mode="r", encoding='utf-8') as meta_json:
            # 在table中进行展示
            meta_dict = json.load(meta_json)

            return meta_dict

    def finished(self):
        res = dict()
        res["account"] = "new2"
        res["web"] = "tiktok"
        res["title"] = "dadadasd"

        success = True
        # 没有account
        if "account" not in res.keys() or "web" not in res.keys():
            QMessageBox.warning(self, "提示", "需要填写账号&web", QMessageBox.Yes)
            success = False
        else:
            # 不希望被覆盖
            if res["account"] in self.accounts.keys():
                is_covered = QMessageBox.warning(self, "提示", "该账号已存在，是否覆盖",  QMessageBox.No | QMessageBox.Yes)
                if is_covered == QMessageBox.No:
                    success = False

        if success:
            self._end_signal.emit(res)
            self.close()