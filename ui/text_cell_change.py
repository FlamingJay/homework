# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\text_cell_change.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(481, 306)
        self.change_finished_btn = QtWidgets.QPushButton(Dialog)
        self.change_finished_btn.setGeometry(QtCore.QRect(200, 250, 75, 31))
        self.change_finished_btn.setStyleSheet("background-color: rgb(85, 170, 0);")
        self.change_finished_btn.setObjectName("change_finished_btn")
        self.cell_content = QtWidgets.QPlainTextEdit(Dialog)
        self.cell_content.setGeometry(QtCore.QRect(20, 20, 441, 221))
        self.cell_content.setObjectName("cell_content")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.change_finished_btn.setText(_translate("Dialog", "修改完成"))

