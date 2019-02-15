#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test.py
# @Author :  ()
# @Link   : 
# @Date   : 2/13/2019, 1:47:06 PM


import sys
from PyQt5 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)
    
    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.closeEvent()


if __name__ == '__main__':
    # app = None
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow('./UI/item_test1.ui')
    w.show()
    sys.exit(app.exec_())