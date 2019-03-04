#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# qt_mainWin.py
# @Author : Ivan-杨杨兮 (523166477@qq.com)
# @Link   : www.cgartech.com
# @Date   : 2019/3/3 下午5:37:49


import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets, uic


# 主窗口 class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)
        # 图标
        # self.ui.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.dirname(__file__)) + '/UI/qt-logo.png'))

        # ----------- 菜单栏 ------------ #
        self.ui.actionSetProjectPath.triggered.connect(self.SetProject)
        # self.ui.pushButton.clicked.connect(self.BTTest)
        # # 实现 treeWidget item 信号和槽连接
        # self.ui.treeWidget_folder.itemClicked['QTreeWidgetItem*', 'int'].connect(self.treeWidget_item_click)

    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()

    def SetProject(self):
        pass


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(os.path.dirname(os.path.dirname(__file__)) +\
        '/UI/AM_MainWin.ui')
    w.show()

    sys.exit(app.exec_()) 