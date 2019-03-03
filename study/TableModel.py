#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ListModel.py
# @Author :  ()
# @Link   : 
# @Date   : 2/15/2019, 9:22:32 AM


import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


data = [
    ['a1', 'a2', 'a3', 'a4'],
    ['b1', 'b2', 'b3', 'b4'],
    ['c1', 'c2', 'c3', 'c4'],
]

headers = ['A', 'B', "C", "D"]

class PaletteTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=[[]], headers=[], parent=None):
        super(PaletteTableModel, self).__init__(parent)

        self.__data = data
        self.__headers = headers

    # 设置行数
    def rowCount(self, parent):
        return len(self.__data)

    # 设置列数
    def columnCount(self, parent):
        return len(self.__data[0])

    # 设置数据
    def data(self, index, role):
        row = index.row()
        column = index.column()

        # 在编辑模式中应用当前值
        if role == QtCore.Qt.EditRole: # 编辑器中编辑形式的数据。
            return self.__data[row][column]

        if role == QtCore.Qt.DecorationRole: # 要以图标形式呈现为装饰的数据
            
            value = QtGui.QColor(255, 0 , 0)

            pixmap = QtGui.QPixmap(26, 26)
            pixmap.fill(value)

            icon = QtGui.QIcon(pixmap)

            return icon

        if role == QtCore.Qt.DisplayRole: # 要以文本形式呈现的关键数据。
            
            value = self.__data[row][column]

            return value

        if role == QtCore.Qt.ToolTipRole: # 工具提示中显示的数据。
            return "color" + self.__data[row][column]

    # 要在模型中启用编辑，还必须实现setData（），并重新实现flags（）以确保ItemIsEditable返回。
    def flags(self, index):
        # 基类实现返回一组标志，标志启用item（ItemIsEnabled），并允许它被选中（ItemIsSelectable）。
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # 编辑数据
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        row = index.row()
        column = index.column()

        if role == QtCore.Qt.EditRole: # 在编辑器中编辑形式的数据。

            self.__data[row][column] = value
            self.dataChanged.emit(index, index) # 数据改变时，通知所有使用该model的项更新
            return True

        return False

    # 设置标题栏信息
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal: # 是否是横向标题
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return 'TEMP'
            else:
                return 'row %d'%(section + 1)

    # --------------------------------------------------------------#
    # 插入多行数据(插入位置， 插入行数， 父项(默认父项为空项))
    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1) # index, first, last

        for i in range(rows):
            value = ['g%d %d'%(rows - i, cl) for cl in range(self.columnCount(None))]
            self.__data.insert(position, value)

        self.endInsertRows()

        return True
    
    # 插入多列数据
    def insertColumns(self, position, columns, parent = QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1) # index, first, last
        
        rowCount = len(self.__data)
        
        for i in range(columns):
            for j in range(rowCount):
                value = 'gc'
                self.__data[j].insert(position, value)

        self.endInsertColumns()

        return True

    # # 删除多行数据（插入位置， 插入行数， 父项(默认父项为空项)）
    # def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
    #     self.beginRemoveRows(parent, position, position + rows - 1)

    #     for i in range(rows):
    #         value = self.__data[position]
    #         self.__data.remove(value)

    #     self.endRemoveRows()

    #     return True

        
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        self.model = PaletteTableModel(data, headers)
        self.ui.listView.setModel(self.model)
        # self.ui.treeView.setModel(self.model)
        self.ui.tableView.setModel(self.model)

        # 插入多行数据
        self.model.insertRows(1, 3)
        self.model.insertColumns(1,2)
        # # 删除多行数据
        # self.model.removeRows(1, 1)
    
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