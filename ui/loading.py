# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\loading.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1130, 753)
        self.movie_label = QtWidgets.QLabel(Dialog)
        self.movie_label.setGeometry(QtCore.QRect(0, 0, 1101, 741))
        self.movie_label.setStyleSheet("QLable{background:transparent}")
        self.movie_label.setText("")
        self.movie_label.setObjectName("movie_label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

