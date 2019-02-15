#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ListModel.py
# @Author :  ()
# @Link   : 
# @Date   : 2/15/2019, 9:22:32 AM


import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


red = QtGui.QColor(255, 0 , 0)
green = QtGui.QColor(0, 255 , 0)
blue = QtGui.QColor(0, 0 , 255)

class PaletteListModel(QtCore.QAbstractListModel):
    def __init__(self, colors=[], parent=None):
        super(PaletteListModel, self).__init__(parent)

        self.__colors = colors

    # 设置行数
    def rowCount(self, parent):
        return len(self.__colors)

    # 获得数据
    def data(self, index, role):
        if role == QtCore.Qt.DecorationRole: # 要以图标形式呈现为装饰的数据
            row = index.row()
            value = self.__colors[row]

            pixmap = QtGui.QPixmap(26, 26)
            pixmap.fill(value)

            icon = QtGui.QIcon(pixmap)

            return icon

        if role == QtCore.Qt.DisplayRole: # 要以文本形式呈现的关键数据。
            row = index.row()
            value = self.__colors[row]

            return value.name()

        if role == QtCore.Qt.ToolTipRole: # 工具提示中显示的数据。
            return "color" + self.__colors[index.row()].name()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        self.model = PaletteListModel([red, green, blue])
        self.ui.listView.setModel(self.model)
        self.ui.treeView.setModel(self.model)
        self.ui.tableView.setModel(self.model)
    
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