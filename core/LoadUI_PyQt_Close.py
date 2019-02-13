#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# spinbox_test1.py
# @Author :  ()
# @Link   : 
# @Date   : 2/13/2019, 9:26:06 AM


import sys
from PyQt5 import QtGui, QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)
    
    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        # 弹出提示对话框
        reply = QtWidgets.QMessageBox.question(self, 
                                               '确认退出', 
                                               "是否要退出程序？", 
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            quit()
        else:
            event.ignore()


if __name__ == '__main__':
    # app = None
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow('./UI/item_test1.ui')
    w.show()
    sys.exit(app.exec_())