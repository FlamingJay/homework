from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QMovie
import os


class LoadingDialog(QDialog):
    def __init__(self, mode):
        super(LoadingDialog, self).__init__()
        self.setFixedSize(500, 500)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.setMinimumHeight(65)

        gif = os.path.abspath(os.path.join(os.getcwd(), ""))
        if mode == "loading":
            gif = os.path.join(gif, "../loading_cat.gif")
        elif mode == "running":
            gif = os.path.join(gif, "loading.gif")

        self.movie_label = QLabel(self)
        self.movie = QMovie(gif)
        self.movie_label.setMovie(self.movie)

        self.movie.start()
        self.show()
