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
        
        self._parentItem = parent
        self._childItems = []
        self._itemData = data

        if parent:
            parent.appendChild(self)

    def typeInfo(self):
        return "None"

    def appendChild(self, item):
        self._childItems.append(item)

    def insertChild(self, position, child):
        if position < 0 or position > len(self._childItems):
            return False
        
        self._childItems.insert(position, child)
        child._parentItem = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self._childItems):
            return False

        child = self._childItems.pop(position)
        child._parentItem = None

    def child(self, row):
        return self._childItems[row]

    def childCount(self):
        return len(self._childItems)

    def columnCount(self):
        return len(self._itemData)

    def data(self):
        return self._itemData

    def setData(self, value):
        self._itemData = value

    def parent(self):
        return self._parentItem

    def row(self):
        if self._parentItem:
            return self._parentItem._childItems.index(self)

        return 0

    def log(self, tablevel=-1):
        output = '--'
        tablevel += 1
        
        for i in range(tablevel):
            output += "\t"

        output =output + "|------" + self._itemData + "\n"

        for child in self._childItems:
            output =output + child.log(tablevel)

        tablevel -= 1
        return output

    def __repr__(self): # 返回一个可以用来表示对象的可打印字符串
        return self.log()


class TransformNode(TreeItem):
    def __init__(self, data, parent):
        super(TransformNode, self).__init__(data, parent)

    def typeInfo(self):
        return "Transform"


class CameraNode(TreeItem):
    def __init__(self, data, parent):
        super(CameraNode, self).__init__(data, parent)

    def typeInfo(self):
        return "Camera"


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        # 设置初始项的内容
        self._rootItem = data
        
        self._checkList = ['Checked', 'Unchecked', 'Unchecked', 'Unchecked', 'Unchecked', 'Unchecked', 'Unchecked', 'Unchecked', 'Unchecked']

    # 设置列数
    def columnCount(self, parent):
        return 3

    # 设置行数
    def rowCount(self, parent):
        # 当父项有效时，rowCount（）应返回0。
        if parent.column() > 0:
            return 0
        
        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    # 返回索引项目存储的数据。
    def data(self, index, role):
        if not index.isValid():
            return None

        # item = index.internalPointer()
        item = self.getItem(index)

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return item.data()
            elif index.column() == 2: # 复选框
                return self._checkList[index.row()]
            else:
                return item.typeInfo()

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                typeInfo = item.typeInfo()

                if typeInfo == "Camera":
                    return QtGui.QIcon(QtGui.QPixmap('./img/qt-logo.png'))

        # 复选框
        if role == QtCore.Qt.CheckStateRole:
            if index.column() == 2:
                if self._checkList[index.row()] == 'Checked':
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked

    # 返回一组标志
    def flags(self, index):

        # 复选框
        if index.column() == 2:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable

        # 基类实现返回一组标志，标志启用item（ItemIsEnabled），并允许它被选中（ItemIsSelectable）。
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    # 编辑数据
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            item = index.internalPointer()

            if role == QtCore.Qt.EditRole:
                item.setData(value)

                return True

        return False

    # 返回给定索引项的父级。如果项目没有父项，则返回无效的QModelIndex。
    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        item = index.internalPointer()
        parentItem = item.parent()

        if parentItem == self._rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    # 返回给定行、列和父索引指定的模型中，项的索引。
    def index(self, row, column, parent):
        # 索引不存在，返回无效索引
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        
        # 如果父项不存在，设置 parentItem = rootItem
        if not parent.isValid():
            parentItem = self._rootItem
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
            if section == 0:
                return "Title"
            else:
                return "typeInfo"

        return None

    # 自定义函数，获取索引项
    def getItem(self, index):
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        
        return self._rootItem
  
    # 插入多列数据
    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1) # index, first, last
                
        for i in range(rows):
            childItem = TreeItem('insert item %d'%i)
            isSuccess = parentItem.insertChild(position, childItem)

        self.endInsertRows()

        return isSuccess
    
    # 删除多行数据（插入位置， 插入行数， 父项(默认父项为空项)）
    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        
        parentItem = self.getItem(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            isSuccess = parentItem.removeChild(position)

        self.endRemoveRows()

        return isSuccess



# 主窗口 class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        rootNode = TreeItem('A')
        childNode1 = TreeItem('A1', rootNode)
        childNode2 = CameraNode('A2', rootNode)
        childNode11 = TreeItem('A21', childNode1)
        childNode12 = TreeItem('A21', childNode1)
        childNode21 = TreeItem('A21', childNode2)
        childNode211 = TransformNode('A21', childNode21)

        print (rootNode)

        # 添加搜索功能
        self._proxyModel = QtCore.QSortFilterProxyModel()
        # View <-----> Proxy Model <------> Data Model

        # 设置 Model
        self.model = TreeModel(rootNode)
        # 设置索引对象
        self._proxyModel.setSourceModel(self.model)
        self._proxyModel.setDynamicSortFilter(True) # 检查属性，开启动态排序
        self._proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive) # 设置大小写不明感
        self._proxyModel.setFilterKeyColumn(0) # 设置检查的列

        self.ui.treeView.setModel(self._proxyModel)

        # 插入行
        self.model.insertRows(1,2)

        # 开启排序功能
        self.ui.treeView.setSortingEnabled(True)

        # self._proxyModel.setFilterRegExp('A1') # 搜索保护 ‘A1’ 的对象

        # 搜索框UI信号
        self.ui.lineEdit.textChanged.connect(self.LE_textChanged)
        # QtCore.QObject.connect(self.ui.lineEdit, QtCore.SIGNAL("textChanged(QString)"), self._proxyModel.setFilterRegExp) # pyqt4
    
    # 搜索
    def LE_textChanged(self, text):
        self._proxyModel.setFilterRegExp(text)

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

    # 插入行
    insterP = w.model.index(0, 0, QtCore.QModelIndex()) # 设置父项
    insterP2 = w.model.index(0, 0, insterP)
    w.model.insertRows(0, 1, insterP)
    w.model.insertRows(0, 1, insterP2)

    sys.exit(app.exec_())