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

    # 设置数据
    def data(self, index, role):
        # 在编辑模式中应用当前值
        if role == QtCore.Qt.EditRole: # 编辑器中编辑形式的数据。
            return self.__colors[index.row()].name()

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

    # 要在模型中启用编辑，还必须实现setData（），并重新实现flags（）以确保ItemIsEditable返回。
    def flags(self, index):
        # 基类实现返回一组标志，标志启用item（ItemIsEnabled），并允许它被选中（ItemIsSelectable）。
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # 编辑数据
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole: # 在编辑器中编辑形式的数据。

            row = index.row()
            color = QtGui.QColor(value)

            if color.isValid():
                self.__colors[row] = color
                self.dataChanged.emit(index, index) # 数据改变时，通知所有使用该model的项更新
                return True
        return False

    # --------------------------------------------------------------#
    # 插入多行数据(插入位置， 插入行数， 父项(默认父项为空项))
    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1) # index, first, last

        for i in range(rows):
            self.__colors.insert(position, QtGui.QColor("#000000"))

        self.endInsertRows()

        return True

    # 删除多行数据（插入位置， 插入行数， 父项(默认父项为空项)）
    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            value = self.__colors[position]
            self.__colors.remove(value)

        self.endRemoveRows()

        return True

        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        self.model = PaletteListModel([red, green, blue])
        self.ui.listView.setModel(self.model)
        self.ui.treeView.setModel(self.model)
        self.ui.tableView.setModel(self.model)

        # 插入多行数据
        self.model.insertRows(1, 3)
        # 删除多行数据
        self.model.removeRows(1, 1)
    
    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()


if __name__ == '__main__':
    # app = None
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow('./study/UI/item_test1.ui')
    w.show()
    sys.exit(app.exec_())