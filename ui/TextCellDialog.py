from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from ui.text_cell_change import Ui_Dialog


class TableCellDialog(QDialog, Ui_Dialog):
    _text_cell_signal = pyqtSignal(str)

    def __init__(self, cell_content=""):
        super(TableCellDialog, self).__init__()
        self.setupUi(self)
        self.cell_content.setPlainText(cell_content)
        self.change_finished_btn.clicked.connect(self.__change_finished)

    def __change_finished(self):
        cur_text = self.cell_content.toPlainText()
        if cur_text == "":
            pass
        else:
            self._text_cell_signal.emit(cur_text)
            self.close()
