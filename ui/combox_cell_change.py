# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\combox_cell_change.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(334, 130)
        self.combox_cell = QtWidgets.QComboBox(Dialog)
        self.combox_cell.setGeometry(QtCore.QRect(20, 20, 291, 41))
        self.combox_cell.setObjectName("combox_cell")
        self.change_finished_btn = QtWidgets.QPushButton(Dialog)
        self.change_finished_btn.setGeometry(QtCore.QRect(120, 80, 75, 31))
        self.change_finished_btn.setStyleSheet("background-color: rgb(85, 170, 0);")
        self.change_finished_btn.setObjectName("change_finished_btn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.change_finished_btn.setText(_translate("Dialog", "修改完成"))

