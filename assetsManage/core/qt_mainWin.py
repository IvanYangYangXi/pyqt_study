#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# qt_mainWin.py
# @Author : Ivan-杨杨兮 (523166477@qq.com)
# @Link   : www.cgartech.com
# @Date   : 2019/3/3 下午5:37:49


import sys, os, re
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import win32gui
import win32con
from ctypes.wintypes import LONG, HWND, UINT, WPARAM, LPARAM, FILETIME
import amConfigure
import amDB
import shutil # 文件夹操作


fileInfo = {}
lastPath = './'
w = None

# ---------------------- TreeItem ---------------------------#
class TreeItem(object):
    def __init__(self, data, parent=None):
        super(TreeItem, self).__init__()
        
        self._parentItem = parent
        self._childItems = []
        self._itemData = data

        if parent:
            parent.appendChild(self)

    def dbData(self):
        value = amDB.findData('assets', 'local="%s"'%self.local())
        return value

    def local(self):
        if self._parentItem == None:
            return self._itemData
        if self._parentItem._itemData == '快速访问':
            return amConfigure.getCollectionPath()[self.row()]
        return (self._parentItem.local()+'/'+self._itemData)

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

        # 初始化
        self.setupModel(data)

    # 初始化  
    def setupModel(self, data):
        # 获取项目根目录
        self._projectPath = data
        # 设置初始项
        self._rootItem = TreeItem(self._projectPath)

        self.updateChild()

    # 设置列数
    def columnCount(self, parent):
        return 1

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
        dbValue = item.dbData()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return item.data()
            elif index.column() == 2:
                return item.local()
            elif index.column() == 1:
                if dbValue:
                    if dbValue[4] == None:
                        return '未登记'
                    elif dbValue[4] == 0:
                        return '未完成'
                    elif dbValue[4] == 1:
                        return '完成'

        # 设置图标
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                # 绘制
                pixmap = QtGui.QPixmap(26, 26)
                pixmap.fill()
                painter = QtGui.QPainter(pixmap)

                if dbValue:
                    if dbValue[4] == None:
                        painter.setBrush(QtCore.Qt.NoBrush)
                    elif dbValue[4] == 0:
                        painter.setBrush(QtGui.QColor('#355263'))
                    elif dbValue[4] == 1:
                        painter.setBrush(QtGui.QColor('#61bd4f'))
                    else:
                        painter.setBrush(QtCore.Qt.NoBrush)
                painter.drawEllipse(3, 3, 20, 20) # 绘制圆
                # painter.drawRoundedRect(3, 3, 20, 20, 10, 10) # 圆角矩形
                painter.end()
                
                return QtGui.QIcon(pixmap) 

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
        if index.data() == '快速访问':
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
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
                return "资产"
            elif section == 1:
                return "状态"
            elif section == 2:
                return "路径"
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

    # 插入多行数据
    def insertRows(self, position, datas, parent = QtCore.QModelIndex()):
        
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + len(datas) - 1) # index, first, last
                
        for i in datas:
            childItem = TreeItem(i)
            isSuccess = parentItem.insertChild(position, childItem)

        self.endInsertRows()

        return isSuccess
    
    # 删除多行数据（删除位置， 删除行数， 父项(默认父项为空项)）
    def removeRows(self, position, rows, parent = QtCore.QModelIndex()):
        
        parentItem = self.getItem(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        isSuccess = False
        for i in range(rows):
            isSuccess = parentItem.removeChild(position)

        self.endRemoveRows()

        return isSuccess

    # 更新子项
    def updateChild(self, parent = QtCore.QModelIndex()):
        # 删除现有子项
        if self.rowCount(parent) > 0:
            self.removeRows(0, self.rowCount(parent), parent)

        parentItem = self.getItem(parent) 
        path = parentItem.local()

        if parent == QtCore.QModelIndex():
            self.insertRows(self.rowCount(parent), ['快速访问'], parent) # 插入快速访问行
            # 设置快速访问项
            # self._collectionItem = TreeItem('快速访问', self._rootItem)

        if parentItem.data() == '快速访问':
            for data in amConfigure.getCollectionPath(): # 获取快速访问路径
                fpath,fname = os.path.split(data)
                self.insertRows(self.rowCount(parent), [fname], parent) # 插入快速访问item
            # print(amConfigure.getCollectionPath())
        elif os.path.isdir(path):
            # path = path + pathAdd # 附加内容到路径
            for data in os.listdir(path): # 获取当前路径下的文件
                if os.path.isdir(os.path.join(path, data)): # 判断是否是目录
                    self.insertRows(self.rowCount(parent), [data], parent) # 插入行


class defaultTreeModel(TreeModel):
    def __init__(self, data, parent=None):
        super(defaultTreeModel, self).__init__(data, parent)
               
        
    # 初始化
    def setupModel(self, data):
        # 获取项目根目录
        self._projectPath = data
        
        if amConfigure.getProjectBranch() == '':
            # ----------- 初始化路径 ---------------- #
            modelPath = self._projectPath+'/3D/scenes/Model'
            if os.path.isdir(self._projectPath):
                if not os.path.exists(self._projectPath+'/3D/scenes/Model'):
                    os.makedirs(self._projectPath+'/3D/scenes/Model') # 创建路径
                if not os.path.exists(self._projectPath+'/3D/scenes/Model/Character'):
                    os.makedirs(self._projectPath+'/3D/scenes/Model/Character') # 角色
                if not os.path.exists(self._projectPath+'/3D/scenes/Model/Prop'):
                    os.makedirs(self._projectPath+'/3D/scenes/Model/Prop') # 道具
                if not os.path.exists(self._projectPath+'/3D/scenes/Model/Scene'):
                    os.makedirs(self._projectPath+'/3D/scenes/Model/Scene') # 场景
        if amConfigure.getProjectBranch() == 'branches':
            # ----------- 初始化路径 ---------------- #
            modelPath = self._projectPath+'/3D/branches/scenes/Model'
            if os.path.isdir(self._projectPath):
                if not os.path.exists(self._projectPath+'/3D/branches/scenes/Model'):
                    os.makedirs(self._projectPath+'/3D/branches/scenes/Model') # 创建路径
                if not os.path.exists(self._projectPath+'/3D/branches/scenes/Model/Character'):
                    os.makedirs(self._projectPath+'/3D/branches/scenes/Model/Character') # 角色
                if not os.path.exists(self._projectPath+'/3D/branches/scenes/Model/Prop'):
                    os.makedirs(self._projectPath+'/3D/branches/scenes/Model/Prop') # 道具
                if not os.path.exists(self._projectPath+'/3D/branches/scenes/Model/Scene'):
                    os.makedirs(self._projectPath+'/3D/branches/scenes/Model/Scene') # 场景

        # 设置初始项
        self._rootItem = TreeItem(modelPath)
        
        self.updateChild()        



# ------------ 文件列表 -------------------#
class DropListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(DropListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True) # 开启可拖放事件
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection) # 按住CTRL可多选
        # 创建右键菜单
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showListRightMenu)
        # 双击打开文件
        self.itemDoubleClicked.connect(self.openFile)

        self._path = '' # 列表显示内容所在目录

    # 拖放进入事件
    def dragEnterEvent(self, event):
        print(event.mimeData().urls())  # 文件所有的路径
        print(event.mimeData().text())  # 文件路径
        print(event.mimeData().formats())  # 支持的所有格式
        if self._path != '':
            if event.mimeData().hasUrls():
                event.accept()
            elif event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
                items = self.selectedItems()
                urls = []
                for i in items:
                    urls.append(QtCore.QUrl('file:///' + os.path.join(self._path, i.text())))
                event.mimeData().setUrls(urls)
                event.accept()
            else:
                event.ignore()
        else:
            showErrorMsg('请先选择目录')
            event.ignore()

    # 拖放移动事件
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        elif event.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    # 拖放释放事件
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            pathes = event.mimeData().urls()
            for path in pathes:
                s = str(path)
                s = s.replace("PyQt5.QtCore.QUrl('file:///",'')
                s = s.replace("')", '')
                if os.path.isfile(s):
                    # fpath,fname = os.path.split(s)
                    if not os.path.exists(self._path):
                        os.makedirs(self._path) # 创建路径
                    shutil.copy(s, self._path)
            self.updateList()

    # 更新文件列表
    def updateList(self):
        self.clear()
        if os.path.exists(self._path):
            for data in os.listdir(self._path): # 获取当前路径下的文件
                if os.path.isfile(os.path.join(self._path, data)): # 判断是否是文件
                    self.addItem(data)

    # 创建右键菜单(list)
    def showListRightMenu(self, pos):
        global lastPath

        # 创建QMenu
        rightMenu = QtWidgets.QMenu(self)
        itemOpen = rightMenu.addAction('打开路径')
        itemImport = rightMenu.addAction('导入文件')
        itemRefresh = rightMenu.addAction('刷新')
        rightMenu.addSeparator() # 分隔器
        itemRename = rightMenu.addAction('重命名')
        # itemAddChild = rightMenu.addAction('添加子项')
        itemDelete = rightMenu.addAction('删除选择项')
        rightMenu.addSeparator() # 分隔器
        # item3.setEnabled(False)
        # # 添加二级菜单
        # secondMenu = rightMenu.addMenu('二级菜单')
        # item4 = secondMenu.addAction('test4')

        items = self.selectedItems()
        # 禁用项
        if len(items) != 1:
            itemRename.setEnabled(False)
        if len(items) == 0:
            itemDelete.setEnabled(False)
        # 将动作与处理函数相关联 
        # item1.triggered.connect()

        action = rightMenu.exec_(QtGui.QCursor.pos()) # 在鼠标位置显示
        # ------------------ 右键事件 ------------------- #
        # 导入文件 amConfigure.getProjectPath()
        if action == itemImport:
            if self._path != '':
                files = QtWidgets.QFileDialog.getOpenFileNames(None, "Find File", lastPath)[0] # 选择文件
                lastPath = os.path.split(files[0])[0] # 设置选择文件的目录
                for path in files:
                    if os.path.isfile(path):
                        if not os.path.exists(self._path):
                            os.makedirs(self._path) # 创建路径
                        shutil.copy(path, self._path) # 复制文件
                self.updateList()
            else:
                showErrorMsg('请先选择目录')
        # 打开路径（在资源管理器中显示）
        if action == itemOpen:
            if os.path.exists(self._path):
                os.startfile(self._path)
        # 刷新
        if action == itemRefresh:
            self.updateList()
        # 重命名
        if action == itemRename:
            value, ok = QtWidgets.QInputDialog.getText(self, "重命名", "请输入文本:", QtWidgets.QLineEdit.Normal, os.path.splitext(items[0].text())[0])
            if ok:
                try:
                    os.rename(os.path.join(self._path, items[0].text()), os.path.join(self._path, value + os.path.splitext(items[0].text())[1]))
                    self.updateList()
                except Exception as e:
                    showErrorMsg('重命名失败，错误代码：%s'%(e))
        # 删除选择项
        if action == itemDelete:
            reply = QtWidgets.QMessageBox.warning(self, "消息框标题",  "确认删除选择项?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply:
                for i in items:
                    path = os.path.join(self._path, i.text())
                    os.remove(path)    #删除文件
                self.updateList()
        
    # 打开文件(可打开外部程序)
    def openFile(self, item):
        os.startfile(os.path.join(self._path, item.text()))


class imgListWidget(DropListWidget):
    def __init__(self, parent=None):
        super(imgListWidget, self).__init__(parent)

        self.setViewMode(self.IconMode)
        self.setIconSize(QtCore.QSize(64, 64))  #Icon 大小
        # self.setSpacing(12)  # 间距大小


    # 更新文件列表
    def updateList(self):
        self.clear()
        if os.path.exists(self._path):
            for data in os.listdir(self._path): # 获取当前路径下的文件
                if os.path.isfile(os.path.join(self._path, data)): # 判断是否是文件
                    ext = os.path.splitext(data)[1].lower()
                    if ext in ['.jpg', '.png', '.jpeg', '.bmp', '.tga', '.gif']:
                        # image = QtGui.QImage()
                        # image.load(os.path.join(self._path, data))
                        # image.save(os.path.join(self._path, data))

                        imgItem = QtWidgets.QListWidgetItem(self)
                        imgItem.setIcon(QtGui.QIcon(os.path.join(self._path, data)))
                        imgItem.setText(data)
                        imgItem.setTextAlignment(QtCore.Qt.AlignHCenter)
                        # imgItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

# ------------------------ 主窗口 class -----------------------------#
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)
        # 图标
        # self.ui.setWindowIcon(QtGui.QIcon(os.path.dirname(os.path.dirname(__file__)) + '/UI/qt-logo.png'))

        # -------------- add widget --------------------#
        # 资产源文件列表
        self.listWidget_sourcefile = DropListWidget(self)
        self.ui.verticalLayout_sourcefile.addWidget(self.listWidget_sourcefile)
        # 导出文件列表
        self.listWidget_expfile = DropListWidget(self)
        self.ui.verticalLayout_expfile.addWidget(self.listWidget_expfile)
        # Rig文件列表
        self.listWidget_rigfile = DropListWidget(self)
        self.ui.verticalLayout_rigfile.addWidget(self.listWidget_rigfile)
        # 贴图文件列表
        self.listWidget_expTex = DropListWidget(self)
        self.ui.verticalLayout_expTex.addWidget(self.listWidget_expTex)
        # 缩略图列表
        self.listWidget_img = imgListWidget(self)
        self.ui.verticalLayout_img.addWidget(self.listWidget_img)

        # ----------- 菜单栏 ------------ #
        self.ui.actionSetProjectPath.triggered.connect(SetProject)
        # self.ui.pushButton.clicked.connect(self.BTTest)

        # --------------- treeView_dir --------------- #
        # 设置 Model
        self.defaultTreeModel = defaultTreeModel(amConfigure.getProjectPath())
        self.ui.treeView_dir.setModel(self.defaultTreeModel)
        # 右键菜单
        self.createRightMenu()

        # 实现 treeWidget item 信号和槽连接
        # self.ui.treeView_dir.selectionModel().selectionChanged.connect(self.setSelection)
        self.ui.treeView_dir.clicked.connect(self.dirTreeItemClicked)

        # --------------- listWidget --------------- #
        self.listWidget_img.clicked.connect(self.listWidget_img_ItemClicked)

    def testEvn(self, env):
        print('1')

    # dirTree item 点击事件
    def dirTreeItemClicked(self, index):
        parentItem = self.defaultTreeModel.getItem(index) 
        path = parentItem.local()

        if os.path.isdir(path) or parentItem.data() == '快速访问': # 判断目录是否存在 或 为 '快速访问' 项
            if self.defaultTreeModel.rowCount(index) == 0 or parentItem.data() == '快速访问':
                # 更新子项
                self.defaultTreeModel.updateChild(index)
            # 展开子项
            if self.defaultTreeModel.rowCount(index) > 0:
                self.ui.treeView_dir.expand(index)
            # 滚动到选择项
            self.ui.treeView_dir.scrollTo(index)

            # fpath,fname = os.path.split(path)

            # ------------- 更新列表 -----------------#
            # 资产文件
            self.listWidget_sourcefile._path = path
            self.listWidget_sourcefile.updateList()
            # 导出文件
            assetsPath = path.replace('scenes/Model', 'assets')
            meshPath = os.path.join(assetsPath, 'Meshes')
            self.listWidget_expfile._path = meshPath
            self.listWidget_expfile.updateList()
            # Rig文件
            rigPath = path.replace('Model', 'Rig')
            self.listWidget_rigfile._path = rigPath
            self.listWidget_rigfile.updateList()
            # 贴图文件
            texPath = os.path.join(assetsPath, 'Textures')
            self.listWidget_expTex._path = texPath
            self.listWidget_expTex.updateList()

            # 缩略图列表
            imgPath = path.replace('scenes', 'images')
            self.listWidget_img._path = imgPath
            self.listWidget_img.updateList()

            if self.listWidget_img.count() > 0:
                imgfolder = self.listWidget_img._path
                imgpath = os.path.join(imgfolder, self.listWidget_img.item(0).text())
                imgpath = imgpath.replace("\\", "/")
                pixmap_mask = QtGui.QPixmap(imgpath)
                self.ui.bt_img.setStyleSheet("QPushButton{border-image: url(%s)}"%(imgpath)) # 按钮样式
                scale = pixmap_mask.height()*(self.ui.bt_img.width() / pixmap_mask.width()) 
                self.ui.bt_img.setFixedHeight(scale) # 设置按钮的高度
            else:
                self.ui.bt_img.setStyleSheet("QPushButton{border-image: url(./)}") # 按钮样式
            print(index.internalPointer())
        else:
            self.defaultTreeModel.removeRows(parentItem.row(), 1, self.defaultTreeModel.parent(index)) # 删除当前项及子项

    # QtWidgets.QPushButton().setMaximumSize
    # listWidget_img item 点击事件
    def listWidget_img_ItemClicked(self, index):
        imgfolder = self.listWidget_img._path
        imgpath = os.path.join(imgfolder, index.data())
        imgpath = imgpath.replace("\\", "/")
        pixmap_mask = QtGui.QPixmap(imgpath)
        self.ui.bt_img.setStyleSheet("QPushButton{border-image: url(%s)}"%(imgpath)) # 按钮样式
        scale = pixmap_mask.height()*(self.ui.bt_img.width() / pixmap_mask.width()) 
        self.ui.bt_img.setFixedHeight(scale) # 设置按钮的高度
        
        
        print(index)

    # 创建右键菜单(treeView_dir)
    def createRightMenu(self):
        # Create right menu for treeview
        self.ui.treeView_dir.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeView_dir.customContextMenuRequested.connect(self.showTreeRightMenu)

    def showTreeRightMenu(self, pos):
        # 创建QMenu
        rightMenu = QtWidgets.QMenu(self.ui.treeView_dir)
        itemOpen = rightMenu.addAction('打开路径')
        itemRefresh = rightMenu.addAction('刷新')
        itemAddChild = rightMenu.addAction('添加子项')
        rightMenu.addSeparator() # 分隔器
        itemRename = rightMenu.addAction('重命名')
        itemRemove = rightMenu.addAction('删除当前项')
        rightMenu.addSeparator() # 分隔器
        itemCollection = rightMenu.addAction('添加到快速访问')
        itemUnCollection = rightMenu.addAction('从快速访问移除')
        # item3.setEnabled(False)
        # # 添加二级菜单
        # secondMenu = rightMenu.addMenu('二级菜单')
        # item4 = secondMenu.addAction('test4')

        index = self.ui.treeView_dir.selectionModel().currentIndex() # 选择的项
        currentItem = self.defaultTreeModel.getItem(index) 
        parentItem = self.defaultTreeModel.parent(index)
        path = currentItem.local()
        # 禁用菜单项
        if not index.data():
            itemRename.setEnabled(False)
            itemAddChild.setEnabled(False)
            itemRemove.setEnabled(False)
            itemCollection.setEnabled(False)
            itemUnCollection.setEnabled(False)
        if index.data() == '快速访问':
            itemOpen.setEnabled(False)
            itemRename.setEnabled(False)
            itemAddChild.setEnabled(False)
            itemRemove.setEnabled(False)
            itemCollection.setEnabled(False)
            itemUnCollection.setEnabled(False)
        if parentItem.data() == '快速访问':
            itemAddChild.setEnabled(False)
            itemCollection.setEnabled(False)
            itemRemove.setEnabled(False)
        else:
            itemUnCollection.setEnabled(False)
        print(path)
        # 将动作与处理函数相关联 
        # item1.triggered.connect()
        action = rightMenu.exec_(QtGui.QCursor.pos()) # 在鼠标位置显示
        # 打开路径
        if action == itemOpen:
            if os.path.exists(path):
                os.startfile(path)
            else:
                showErrorMsg('目录不存在')
        # 添加子项
        if action == itemAddChild:
            if os.path.exists(path):
                value, ok = QtWidgets.QInputDialog.getText(self, "添加子项", "请输入文本:", QtWidgets.QLineEdit.Normal, 'NewForder')
                if not os.path.isdir(os.path.join(path, value.strip())):
                    os.makedirs(os.path.join(path, value.strip()))
                    self.defaultTreeModel.updateChild(index) # 更新子项
                else:
                    showErrorMsg('目录已存在')
        # 刷新
        if action == itemRefresh:
            # 更新子项
            self.defaultTreeModel.updateChild(index)
        # 重命名
        if action == itemRename:
            value, ok = QtWidgets.QInputDialog.getText(self, "重命名", "请输入文本:", QtWidgets.QLineEdit.Normal, currentItem.data())
            if ok:
                try:
                    os.rename(path, os.path.join(os.path.split(path)[0], value))
                    currentItem.setData(value)
                except Exception as e:
                    showErrorMsg('重命名失败，错误代码：%s'%(e))
        # 删除选择项
        if action == itemRemove:
            reply = QtWidgets.QMessageBox.warning(self, "消息框标题",  "确认删除选择项?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reply:
                os.removedirs(path)    # 递归删除文件夹
                self.defaultTreeModel.removeRows(currentItem.row(), 1, self.defaultTreeModel.parent(index))
        # 从快速访问移除
        if action == itemUnCollection:
            self.defaultTreeModel.removeRows(currentItem.row(), 1, self.defaultTreeModel.parent(index))
            amConfigure.removeCollectionPath(path)
        # 添加到快速访问
        if action == itemCollection:
            amConfigure.addCollectionPath(path)

    def setSelection(self, selected, deselected):
        pass
        
    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()




def updatePath():
    projectPath = amConfigure.getProjectPath()
    # SM_S
    SM_Character_s = projectPath + '/3D/scenes/Model/Character'
    SM_Prop_s = projectPath + '/3D/scenes/Model/Prop'
    SM_Scene_s = projectPath + '/3D/scenes/Model/Scene'
    # SM_A
    SM_Character_a = projectPath + '/3D/assets/Model/Character'
    SM_Prop_a = projectPath + '/3D/assets/Model/Prop'
    SM_Scene_a = projectPath + '/3D/assets/Model/Scene'
    # SK_S
    SK_Character_s = projectPath + '/3D/scenes/Rig/Character'
    SK_Prop_s = projectPath + '/3D/scenes/Rig/Prop'
    SK_Scene_s = projectPath + '/3D/scenes/Rig/Scene'
    # SM_A
    SM_Character_a = projectPath + '/3D/assets/Model/Character'
    SM_Prop_a = projectPath + '/3D/assets/Model/Prop'
    SM_Scene_a = projectPath + '/3D/assets/Model/Scene'

    for i in os.listdir(projectPath + '/3D/scenes/Model'):
        fileInfo[i] = []
        print(fileInfo)
    # for parent, dirname, filenames in os.walk(SM_Character_s):
    #     # print(parent)
    #     # print(dirname)
    #     # print(filenames)
    #     a = re.match(r'(.+[\\/])(.+$)', parent).group(2)
    #     print(a)
    

# 错误信息
def showErrorMsg(msg):
    print(msg)

# 选择文件夹
def browse():
    directory = ''
    if amConfigure.getProjectPath() != None:
        if os.path.isdir(amConfigure.getProjectPath()):
            directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Find Dir", \
                amConfigure.getProjectPath())
        else:
            directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Find Dir", \
                QtCore.QDir.currentPath())
    else:
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Find Dir", \
            QtCore.QDir.currentPath())

    return directory

# 设置工程目录
def SetProject():
    directory = browse()
    if directory != '':
        amConfigure.setProjectPath(directory)
        w.defaultTreeModel.setupModel(amConfigure.getProjectPath()) # 更新 defaultTreeModel 
    elif not os.path.isdir(amConfigure.getProjectPath()):
        showErrorMsg('工程目录不存在')
        # w.close() # 退出窗口程序


def main():
    # print(os.path.isdir(amConfigure.getProjectPath()))
    # 启动窗口
    global w
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(os.path.dirname(os.path.dirname(__file__)) +\
        '/UI/AM_MainWin.ui')
    w.show()

    # 检查工程目录是否存在,不存在则设置工程目录
    if not os.path.isdir(amConfigure.getProjectPath()):
        SetProject()
    else:
        amConfigure.getProjectPath()

    sys.exit(app.exec_()) 


if __name__ == '__main__':
    main()
    