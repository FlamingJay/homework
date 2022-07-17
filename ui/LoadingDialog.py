from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore
import os


class LoadingDialog(QDialog):
    def __init__(self, mode):
        super(LoadingDialog, self).__init__()
        self.setFixedSize(290, 290)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)

        self.close_btn = QPushButton("关闭提示", self)
        self.close_btn.setGeometry(QtCore.QRect(80, 250, 80, 40))
        self.close_btn.setStyleSheet("background-color: rgb(85, 170, 0);")
        self.close_btn.clicked.connect(self.__stop_show)

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
        self.movie_label.setGeometry(QtCore.QRect(0, 0, 240, 240))
        self.movie_label.setStyleSheet("background:transparent")
        self.movie = QMovie(gif)
        self.movie_label.setMovie(self.movie)

        self.movie.start()
        self.show()



    def __stop_show(self):
        self.close()