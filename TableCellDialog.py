from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from cell_change import Ui_Dialog


class TableCellDialog(QDialog, Ui_Dialog):
    _content_back_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TableCellDialog, self).__init__(parent)
        self.setupUi(self)
        self.change_finished_btn.clicked.connect(self.__change_finished)

    def set_text(self, cell_content):
        self.cell_content.setPlainText(cell_content)

    def __change_finished(self):
        cur_text = self.cell_content.toPlainText()
        if cur_text == "":
            pass
        else:
            self._content_back_signal.emit(cur_text)
            self.close()
