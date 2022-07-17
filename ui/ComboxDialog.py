from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from ui.combox_cell_change import Ui_Dialog


class ComboxDialog(QDialog, Ui_Dialog):
    _combox_cell_signal = pyqtSignal(str)

    def __init__(self, mode=""):
        super(ComboxDialog, self).__init__()
        self.setupUi(self)
        self.__fill_combox(mode)
        self.change_finished_btn.clicked.connect(self.__change_finished)

    def __fill_combox(self, mode):
        if mode == "web":
            self.combox_cell.addItems(['youtube', 'tiktok'])
        elif mode == "video_type":
            self.combox_cell.addItems(['short', 'long'])
        elif mode == "use_file_title":
            self.combox_cell.addItems(['true', 'false'])

    def __change_finished(self):
        cur_text = self.combox_cell.currentText()
        if cur_text == "":
            pass
        else:
            self._combox_cell_signal.emit(cur_text)
            self.close()
