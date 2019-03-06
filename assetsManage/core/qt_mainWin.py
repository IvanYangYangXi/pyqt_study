#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# qt_mainWin.py
# @Author : Ivan-杨杨兮 (523166477@qq.com)
# @Link   : www.cgartech.com
# @Date   : 2019/3/3 下午5:37:49


import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import amConfigure


# ---------------------- TreeItem ---------------------------#
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

    # def columnCount(self):
    #     return len(self._itemData)

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

# ------------------- TreeModel -----------------------------#
class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        # 设置初始项的内容
        self._rootItem = data

        # self.setupModelData()
        
    # 设置列数
    def columnCount(self, parent):
        return 2

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
            # elif index.column() == 2: # 复选框
            #     return self._checkList[index.row()]
            else:
                return item.typeInfo()

        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                typeInfo = item.typeInfo()

                if typeInfo == "Camera":
                    return QtGui.QIcon(QtGui.QPixmap('./img/qt-logo.png'))

        # # 复选框
        # if role == QtCore.Qt.CheckStateRole:
        #     if index.column() == 2:
        #         if self._checkList[index.row()] == 'Checked':
        #             return QtCore.Qt.Checked
        #         else:
        #             return QtCore.Qt.Unchecked

    # 返回一组标志
    def flags(self, index):

        # # 复选框
        # if index.column() == 2:
        #     return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable

        # 基类实现返回一组标志，标志启用item（ItemIsEnabled），并允许它被选中（ItemIsSelectable）。
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    # 编辑数据
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            item = index.internalPointer()

            if role == QtCore.Qt.EditRole:
                if index.column() == 0:
                    item.setData(value)
                    self.dataChanged.emit(index, index) # 更新Model的数据

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

    # 初始化数据
    def setupModelData(self, data, parent):
        pass


class defaultTreeModel(TreeModel):
    def __init__(self, data, parent=None):
        super(defaultTreeModel, self).__init__(data, parent)
        
        self._rootItem = TreeItem('assets')
        
        self._character = TreeItem('角色', self._rootItem)
        self._character = TreeItem('道具', self._rootItem)
        self._character = TreeItem('场景', self._rootItem)


# 选择文件夹
def browse():
    if amConfigure.getProjectPath() == None:
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Find Dir", \
            QtCore.QDir.currentPath())
    else:
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Find Dir", \
            amConfigure.getProjectPath())

    return directory

# 设置工程目录
def SetProject():
        directory = browse()
        if directory:
            amConfigure.setProjectPath(directory)



# ------------------------ 主窗口 class -----------------------------#
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)
        # 图标
        # self.ui.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.dirname(__file__)) + '/UI/qt-logo.png'))
        
        # 设置 Model
        self.moedel = defaultTreeModel('0')
        self.ui.treeView_dir.setModel(self.moedel)

        # ----------- 菜单栏 ------------ #
        self.ui.actionSetProjectPath.triggered.connect(SetProject)
        # self.ui.pushButton.clicked.connect(self.BTTest)
        # # 实现 treeWidget item 信号和槽连接
        # self.ui.treeWidget_folder.itemClicked['QTreeWidgetItem*', 'int'].connect(self.treeWidget_item_click)

    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()


def main():
    # 启动窗口
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(os.path.dirname(os.path.dirname(__file__)) +\
        '/UI/AM_MainWin.ui')
    w.show()

    # 检查工程目录是否存在,不存在则设置工程目录
    if amConfigure.getProjectPath() == None:
        SetProject()

    sys.exit(app.exec_()) 


if __name__ == '__main__':
    main()
    