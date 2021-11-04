#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author : Ivan-杨杨兮 (523166477@qq.com)

from posixpath import abspath
import sys
import os
from PyQt5 import QtWidgets, uic, QtCore, QtGui, Qt
import shutil


# QtWidgets.QTreeWidget.clear()
# QtWidgets.QTreeWidgetItem(treeWidget)
# QtGui.QIcon(fileName)
# QtWidgets.QTreeWidget.
# QtCore.Qt.MatchFlag.MatchExactly
# QtWidgets.QTreeWidgetItem.setExpanded(True)
# QtWidgets.QTreeWidget.setAcceptDrops(True)
# QtWidgets.QTreeWidget.
# QtWidgets.QTreeWidgetItem.checkState


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)
        # self.setWindowModality(0)

        self.folderPath = 'C://'
        self.exportFolder = os.path.join(os.path.expanduser('~'), "Desktop") # 桌面的路径
        self.files = []
        self.currentfiles = []

        self.maxStep = 1
        self.total_num = 0
        self.step = self.total_num * (100/self.maxStep)

        #载入进度条控件
        self.pbar = QtWidgets.QProgressBar()
        self.pbar.setGeometry(0, 0, 200, 5)
        # self.pbar.resize(200, 10)
        #设置进度条的范围
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(100)
        self.pbar.setValue(int(self.step))

        self.ui.statusBar().showMessage('准备')
        self.ui.statusbar.addPermanentWidget(self.pbar) # ,stretch=4

        self.ui.treeWidget.setAcceptDrops(True)
        #设置列数
        self.ui.treeWidget.setColumnCount(2)
        #设置树形控件头部的标题
        self.ui.treeWidget.setHeaderLabels(['文件', '路径'])
        #设置树形控件的列的宽度
        self.ui.treeWidget.setColumnWidth(0,500)

        # #设置根节点
        # root=QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        # root.setText(0,'Root')
        # # root.setIcon(0,QtGui.QIcon('./images/root.png'))

        self.ui.bt_selectFiles.clicked.connect(lambda: self.chooseFile())
        self.ui.bt_exportFlies.clicked.connect(lambda: self.exportFlie())
        self.ui.bt_clearFiles.clicked.connect(lambda: self.clearFile())
        self.ui.bt_openFolder.clicked.connect(lambda: self.openFolder())

    def clearFile(self):
        self.ui.treeWidget.clear()
        self.files = []

    def chooseFile(self):
        self.currentfiles, filetype = QtWidgets.QFileDialog.getOpenFileNames(self,
                '选择文件',
                self.folderPath,   #起始路径
                'Image Files All Files (*)') #设置文件扩展名过滤,注意用双分号间隔
        if self.currentfiles:
            self.folderPath = os.path.split(self.currentfiles[0])[0]
            self.files.extend(self.currentfiles)
            # print(self.folderPath + "+" + os.path.split(selfiles[0])[1])
            self.setList()

    def setList(self):
        self.ui.label.setText('文件数量: ' + str(len(self.files)))
        # print(self.files)

        for i in self.currentfiles:
            fileName = i
            filePathArray = fileName.split('/')
            
            for x in range(len(filePathArray)):
                splitfilePath = '/'.join(filePathArray[0:(x+1)])
                # print(splitfilePath)
                # 查找所有子项
                findItems = self.ui.treeWidget.findItems(splitfilePath,QtCore.Qt.MatchRecursive, 1)
                # print(splitfilePath)
                # print(findItems)
                if x == 0:
                    if findItems == []:
                        #设置根节点
                        parentItem = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
                        parentItem.setText(0, filePathArray[x])
                        parentItem.setText(1, splitfilePath)
                    else:
                        parentItem = findItems[0]
                else:
                    if findItems == []:
                        #设置子节点
                        childItem = QtWidgets.QTreeWidgetItem()
                        childItem.setText(0, filePathArray[x])
                        childItem.setText(1, splitfilePath)
                        # childItem.setIcon(0,QtGui.QIcon('./images/IOS.png'))
                        # 判断是文件还是文件夹
                        if os.path.isfile(splitfilePath):
                            # 设置节点的状态(设置指定列的选中状态)
                            childItem.setCheckState(0,QtCore.Qt.Checked)
                        parentItem.addChild(childItem)

                        parentItem = childItem
                    else:
                        parentItem = findItems[0]

                parentItem.setExpanded(True)

        # if rootCount == 0:  
            # #设置根节点
            # rootItem = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
            # rootItem.setText(0,'Desktop')
            # rootItem.setText(1, os.path.join(os.path.expanduser('~'), "Desktop")) # 桌面的路径
            # root.setIcon(0,QtGui.QIcon('./images/root.png'))

    def exportFlie(self):
        savePath = QtWidgets.QFileDialog.getExistingDirectory(self, "选择文件保存路径", self.exportFolder)

        if savePath:
            self.exportFolder = savePath

            exportFlies = []
            for i in self.files:
                # 查找所有子项
                findItems = self.ui.treeWidget.findItems(i,QtCore.Qt.MatchRecursive, 1)
                # 是否选中
                if findItems[0].checkState(0) == QtCore.Qt.Checked:
                    exportFlies.append(i)

            if exportFlies:
                # 进度条
                self.pbar.setValue(0)
                self.total_num = 0
                self.maxStep = len(exportFlies)
                self.ui.statusBar().showMessage('正在复制到 ' + savePath)

                for i in exportFlies:
                    saveFilePath = savePath + '/' + i.split('/', 1)[1]
                    # print(os.path.split(saveFilePath)[0])
                    if not os.path.exists(os.path.split(saveFilePath)[0]):
                        # 如果不存在则创建目录
                        os.makedirs(os.path.split(saveFilePath)[0]) # 创建目录操作函数

                    # 复制文件
                    shutil.copyfile(i, saveFilePath)
                
                    # 更新进度条
                    self.total_num += 1
                    self.step = self.total_num * (100/self.maxStep)
                    if self.step >=100:
                        self.ui.statusBar().showMessage('完成')
                    self.pbar.setValue(int(self.step)) 

    # 拖拽文件
    # 子窗口无法拖拽, 父类设置好解决了此问题
    def dragEnterEvent(self,e):
        # print(e)
        if e.mimeData().hasText():
            e.accept()

    def dropEvent(self,e):
        filePathTex = e.mimeData().text()
        filePathList = filePathTex.split('\n')
        for i in range(len(filePathList)):
            filePathList[i] = filePathList[i].replace('file:///', '', 1) #去除文件地址前缀的特定字符
            # 删除列表中所有空元素
            if filePathList[i] == ' ' or filePathList[i] == '':
                filePathList.remove(filePathList[i])
        self.currentfiles = filePathList
        self.files.extend(self.currentfiles)
        self.setList()

    def openFolder(self):
        os.startfile(self.exportFolder)

    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()



if __name__ == '__main__':
    # app = None
    app = QtWidgets.QApplication(sys.argv)
    getabspath = os.path.abspath(os.path.dirname(__file__))
    w = MainWindow(getabspath + '/UI/Main.ui')
    # w = ProgressBar()
    # w = MainWindow('./UI/item_test1.ui')
    w.show()
    sys.exit(app.exec_())