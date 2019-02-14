#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SimpleTreeViewModel.py
# @Author :  ()
# @Link   : 
# @Date   : 2/14/2019, 10:09:02 AM

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class TreeItem(object):
    def __init__(self, data, parent=None):
        super(TreeItem, self).__init__()
        
        self.parentItem = parent
        self.childItems = []
        self.itemData = data

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        # 设置标题行的内容
        self.rootItem = TreeItem(("Title","Summary"))
        self.setupModelData(self.rootItem)

    # 设置列数
    def columnCount(self, parent):
        return 2

    # 设置行数
    def rowCount(self, parent):
        # 当父项有效时，rowCount（）应返回0。
        if parent.column() > 0:
            return 0
        
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    # # 返回索引项目存储的数据。
    # def data(self, index, role):
    #     if not index.isValid():
    #         return None

    #     if role != QtCore.Qt.DisplayRole:
    #         return None

    #     item = index.internalPointer()

    #     return item.data(index.column())

    # 返回给定行、列和父索引指定的模型中，项的索引。
    def index(self, row, column, parent):
        # 索引不存在，返回无效索引
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        
        # 如果父项不存在，设置 parentItem = rootItem
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            # 子类中重写此函数时，调用createIndex()以生成其他组件用于项的模型索引。
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    # # 返回给定索引项的父级。如果项目没有父项，则返回无效的QModelIndex。
    # def parent(self, index):
    #     if not index.isValid():
    #         return QtCore.QModelIndex()

    #     childItem = index.internalPointer()
    #     parentItem = childItem.parent()

    #     if parentItem == self.rootItem:
    #         return QtCore.QModelIndex()

    #     return self.createIndex(parentItem.row(), 0, parentItem)
        
    # 设置标题行
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def setupModelData(self, parent):
        parents = [parent]
        parents[-1].appendChild(TreeItem(("aa"), parents[-1]))
        parents[0].appendChild(TreeItem(("bb"), parents[0]))
        parents[0].appendChild(TreeItem(("bbbbb"), parents[0]))

a = [70,90,20,50]

# 主窗口 class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        # 设置 Model
        self.model = TreeModel(a)
        self.ui.treeView.setModel(self.model)

        # 设置 Item
        # self.item = SpinBoxDelegate()
        # self.ui.tableView.setItemDelegate(self.item)

        # for row in range(4):
        #     for column in range(2):
        #         index = self.model.index(row, column, QtCore.QModelIndex())
        #         self.model.setData(index, (row + 1)*(column + 1))
    
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