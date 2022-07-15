from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from loading import Ui_Dialog
from PyQt5.QtGui import QMovie
import os


# class LoadingDialog(QDialog, Ui_Dialog):
#     def __init__(self, parent=None):
#         gif = os.path.abspath(os.path.join(os.getcwd(), "resource", "loading.gif"))
#         self.movie = QMovie(gif)
#         self.movie.setCacheMode(QMovie.CacheAll)
#         self.label.setMovie(self.movie)

class LoadingDialog(QDialog):
    def __init__(self):
        super(LoadingDialog, self).__init__()
        self.setFixedSize(500, 500)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.setMinimumHeight(65)

        self.movie_label = QLabel(self)

        self.movie = QMovie("loading_cat.gif")
        self.movie_label.setMovie(self.movie)

        self.movie.start()

        self.show()



    def handleFrameChange(self):
        pixmap = self.movie.currentPixmap()
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())
