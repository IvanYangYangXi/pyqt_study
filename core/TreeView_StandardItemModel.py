#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# TreeView_StandardItemModel.py
# @Author : Ivan-杨杨兮 (523166477@qq.com)
# @Link   : www.cgartech.com
# @Date   : 2019/2/14 下午7:19:02


import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class TreeModel(QtGui.QStandardItemModel):
    def __init__(self, row, column, parent=None):
        super(TreeModel, self).__init__(row, column, parent)

        self.setHeaderData(0, QtCore.Qt.Horizontal, "DA")
        self.setHeaderData(1, QtCore.Qt.Horizontal, "DB")
        self.setHeaderData(2, QtCore.Qt.Horizontal, "DC")
        
    def addItem(self, dataA, dataB, dataC):
        self.insertRow(0)
        self.setData(self.index(0, 0), dataA)
        self.setData(self.index(0, 1), dataB)
        self.setData(self.index(0, 2), dataC)


# 主窗口 class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        # 设置 Model
        self.model = TreeModel(0, 3)
        self.ui.treeView.setModel(self.model)

        self.model.addItem('aa', 'bb', 'cc')
        self.model.addItem('a1', 'b1', 'c1')


    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()


if __name__ == '__main__':
    # app = None
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow('./UI/item_test1.ui')
    w.show()
    sys.exit(app.exec_())