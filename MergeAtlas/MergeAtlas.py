#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author : Ivan-杨杨兮 (523166477@qq.com)

import sys
import os
from PyQt5 import QtWidgets, uic, QtCore, QtGui
import PIL.Image as Image
from queue import Queue


# QtWidgets.QListWidget.setItemWidget()
# QtWidgets.QPushButton.clicked.connect()
# QtWidgets.QListWidget.itemAt
# QtWidgets.QListWidget.currentRow
# QtWidgets.QListWidget.clear()
# QtWidgets.QLabel.setText('')
# QtCore.Qt.CustomContextMenu
# QtWidgets.QRadioButton.objectName



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)
        # PyQt5 加载ui文件方法
        self.ui = uic.loadUi(uiPath, self)

        self.folderPath = 'C://'
        self.files = []
        self.image_sizeU = 512  # 每张小图片的大小
        self.image_sizeV = 512  # 每张小图片的大小
        self.image_row = 4  # 图片行，也就是合并成一张图后，一共有几行
        self.image_column = 4  # 图片列，也就是合并成一张图后，一共有几列

        self.ui.bt_selectImgs.clicked.connect(lambda: self.chooseFile())
        self.ui.bt_clearImgs.clicked.connect(lambda: self.clearFile())
        self.ui.bt_combineImgs.clicked.connect(lambda: self.combineImgs())
        #右键菜单
        self.ui.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.customContextMenuRequested.connect(self.rightMenu)

        #单选框，当状态改变时信号触发事件
        self.ui.radioButton.toggled.connect(lambda: self.btnstate(self.ui.radioButton))
        self.ui.radioButton_2.toggled.connect(lambda: self.btnstate(self.ui.radioButton_2))

    def btnstate(self,btn):
        # 输出按钮1与按钮2的状态
        if btn.objectName()=='radioButton':
            if btn.isChecked()==True:
                # print(btn.text()+" is selected")
                self.image_sizeU = 1024 
                self.image_sizeV = 512
                self.image_row = 4
                self.image_column = 2

        if btn.objectName()=='radioButton_2':
            if btn.isChecked()==True:
                # print(btn.text()+" is selected")
                self.image_sizeU = 512 
                self.image_sizeV = 512
                self.image_row = 4
                self.image_column = 4

    def combineImgs(self):
        # print('combineImgs')
        savefile, filetype = QtWidgets.QFileDialog.getSaveFileName(self, "文件保存", self.folderPath,"tga Files (*.tga);;png Files (*.png)")

        if savefile:
            self.folderPath = os.path.split(savefile[0])[0]
            to_image = Image.new('RGBA', (self.image_column * self.image_sizeU, self.image_row * self.image_sizeV), (255,255,255,255))  # 创建一个新图
            # 循环遍历，把每张图片按顺序粘贴到对应位置上
            total_num = 0
            for y in range(1, self.image_row + 1):
                for x in range(1, self.image_column + 1):
                    # print(str(self.image_column * (y - 1) + x - 1))
                    # print(self.files) 
                    from_image = Image.open(self.files[self.image_column * (y - 1) + x - 1]).resize((self.image_sizeU, self.image_sizeV), Image.ANTIALIAS)
                    to_image.paste(from_image, ((x - 1) * self.image_sizeU, (y - 1) * self.image_sizeV))
                    total_num += 1
                    if total_num == len(self.files):
                        break
                if total_num == len(self.files):
                        break
            return to_image.save(savefile)  # 保存新图

    def clearFile(self):
        self.ui.listWidget.clear()
        self.files = []

    def chooseFile(self):
        selfiles, filetype = QtWidgets.QFileDialog.getOpenFileNames(self,
                '选择图片',
                self.folderPath,   #起始路径
                'Image Files (*.png , *.jpg , *.tga);;All Files (*)') #设置文件扩展名过滤,注意用双分号间隔
        self.folderPath = os.path.split(selfiles[0])[0]
        self.files.extend(selfiles)
        self.setList()
        
    def setList(self):
        self.ui.listWidget.clear()

        self.ui.label.setText('图片数量: ' + str(len(self.files)))

        for i in self.files:
            fileName = i
            self.ui.listWidget.setIconSize(QtCore.QSize(30, 30))
            icon = QtGui.QIcon(fileName)
            item = QtWidgets.QListWidgetItem(icon, str(self.files.index(i)) + '. ' + os.path.split(fileName)[1]) # 实例化一个Item
            self.ui.listWidget.addItem(item)

    def rightMenu(self, position):
        #弹出菜单
        popMenu = QtWidgets.QMenu(self)
        moveUpAct =QtWidgets.QAction("上移",popMenu)
        moveDownAct =QtWidgets.QAction("下移",popMenu)
        delAct =QtWidgets.QAction(u'删除', popMenu)
        #查看右键时是否在item上面
        if self.ui.listWidget.itemAt(position):
            if self.ui.listWidget.currentRow() != 0:
                popMenu.addAction(moveUpAct)
            if self.ui.listWidget.currentRow() != len(self.files)-1: 
                popMenu.addAction(moveDownAct)
            popMenu.addAction(delAct)

        moveUpAct.triggered.connect(self.moveUp)
        moveDownAct.triggered.connect(self.moveDown)
        delAct.triggered.connect(self.delItem)

        popMenu.exec_(QtGui.QCursor.pos())

    def moveUp(self):
        currentID = self.ui.listWidget.currentRow()
        # print('move up ' + str(currentID))
        itemA = self.files[currentID]
        itemB = self.files[currentID - 1]
        self.files[currentID] = itemB
        self.files[currentID - 1] = itemA
        self.setList()

    def moveDown(self):
        currentID = self.ui.listWidget.currentRow()
        # print('move down ' + str(currentID))
        itemA = self.files[currentID]
        itemB = self.files[currentID + 1]
        self.files[currentID] = itemB
        self.files[currentID + 1] = itemA
        self.setList()

    def delItem(self):
        currentID = self.ui.listWidget.currentRow()
        # print('del ' + str(currentID))
        del(self.files[currentID])
        self.setList()

    def closeEvent(self, event):
        '''
        重写closeEvent方法
        '''
        event.accept()
        quit()


if __name__ == '__main__':
    # app = None
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow('./UI/Main.ui')
    # w = MainWindow('./UI/item_test1.ui')
    w.show()
    sys.exit(app.exec_())