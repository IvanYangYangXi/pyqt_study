#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# TableView_spinbox.py
# @Author :  ()
# @Link   : 
# @Date   : 2/13/2019, 9:26:06 AM


import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

# Item class
class SpinBoxDelegate(QtWidgets.QStyledItemDelegate):
    '''
    '''
    # createEditor 返回用于更改模型数据的小部件，可以重新实现以自定义编辑行为。
    def createEditor(self, parent, option, index):
        editor = QtWidgets.QSpinBox(parent)
        editor.setFrame(False)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        # 设置 Model
        self.model = QtGui.QStandardItemModel(4, 2)
        self.ui.tableView.setModel(self.model)

        # 设置
    
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