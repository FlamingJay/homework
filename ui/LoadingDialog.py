from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
import os


class LoadingDialog(QDialog):
    def __init__(self, mode):
        super(LoadingDialog, self).__init__()
        self.setFixedSize(240, 240)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)

        gif = os.path.abspath(os.path.join(os.getcwd(), 'ui'))
        if mode == "loading":
            gif = os.path.join(gif, 'loading_cat.gif')
        elif mode == "running":
            gif = os.path.join(gif, 'loading.gif')
        elif mode == "merge_editor":
            gif = os.path.join(gif, 'working.gif')
        elif mode == "single_editor":
            gif = os.path.join(gif, 'working.gif')

        self.movie_label = QLabel(self)

        self.movie_label.setStyleSheet("background:transparent")
        self.movie = QMovie(gif)
        self.movie_label.setMovie(self.movie)

        self.movie.start()
        self.show()
