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
        
        self.__parentItem = parent
        self.__childItems = []
        self.__itemData = data

        if parent:
            parent.appendChild(self)

    def appendChild(self, item):
        self.__childItems.append(item)

    def child(self, row):
        return self.__childItems[row]

    def childCount(self):
        return len(self.__childItems)

    def columnCount(self):
        return len(self.__itemData)

    def data(self):
        return self.__itemData
        # try:
        #     return self.__itemData[column]
        # except IndexError:
        #     return None

    def parent(self):
        return self.__parentItem

    def row(self):
        if self.__parentItem:
            return self.__parentItem.__childItems.index(self)

        return 0

    def log(self, tablevel=-1):
        output = '--'
        tablevel += 1
        
        for i in range(tablevel):
            output += "\t"

        output =output + "|------" + self.__itemData + "\n"

        for child in self.__childItems:
            output =output + child.log(tablevel)

        tablevel -= 1
        return output

    def __repr__(self): # 返回一个可以用来表示对象的可打印字符串
        return self.log()


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        # 设置标题行的内容
        self.__rootItem = data
        # self.setupModelData(self.__rootItem)

    # 设置列数
    def columnCount(self, parent):
        return 1

    # 设置行数
    def rowCount(self, parent):
        # 当父项有效时，rowCount（）应返回0。
        if parent.column() > 0:
            return 0
        
        if not parent.isValid():
            parentItem = self.__rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    # 返回一组标志
    def flags(self, index):
        # 基类实现返回一组标志，标志启用item（ItemIsEnabled），并允许它被选中（ItemIsSelectable）。
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # 返回给定索引项的父级。如果项目没有父项，则返回无效的QModelIndex。
    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        item = index.internalPointer()
        parentItem = item.parent()

        if parentItem == self.__rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    # 返回给定行、列和父索引指定的模型中，项的索引。
    def index(self, row, column, parent):
        # 索引不存在，返回无效索引
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        
        # 如果父项不存在，设置 parentItem = rootItem
        if not parent.isValid():
            parentItem = self.__rootItem
        else:
            parentItem = parent.internalPointer()

        item = parentItem.child(row)
        if item:
            # 子类中重写此函数时，调用createIndex()以生成其他组件,用于项的模型索引。
            return self.createIndex(row, column, item)
        else:
            return QtCore.QModelIndex()

    # 设置标题行
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return "Title"

        return None

    # 返回索引项目存储的数据。
    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            return item.data()

  
    # def setupModelData(self, parent):
    #     parents = [parent]
    #     parents[-1].appendChild(TreeItem(("aa",'b1'), parents[-1]))
    #     parents[0].appendChild(TreeItem(("bb",'b2'), parents[0]))


a = [70,90,20,50]

# 主窗口 class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        # 设置 Model
        self.model = TreeModel(rootNode)
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
    rootNode = TreeItem('A')
    childNode0 = TreeItem('A1', rootNode)
    childNode1 = TreeItem('A2', rootNode)
    childNode2 = TreeItem('A21', childNode1)

    print (rootNode)

    # app = None
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow('./study/UI/item_test1.ui')
    w.show()
    sys.exit(app.exec_())