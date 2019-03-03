#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test.py
# @Author :  ()
# @Link   : 
# @Date   : 2/13/2019, 1:47:06 PM


#coding=utf-8
# from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QDialog,QWidget, QFileDialog, QPushButton, QLineEdit, QGridLayout
import sys, os
 
class MyLoadTskList(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.initTaskList()
    def initTaskList(self):
        global connectserver
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.model = QStandardItemModel()
        self.ui.btsure.clicked.connect(self.test)
        
        tsklist = [u'北京', u'南京', u'海南', u'青岛', u'西安']
        #model = QStandardItemModel()
        for task in tsklist:
            item = QStandardItem(QString(task))
            item.setCheckState(False)
            item.setCheckable(True)
            self.model.appendRow(item)
            self.ui.listView.setModel(self.model)
    def test(self):
        #获取选中的item的index
        print ("hello this is LoadTskList")
        lsd = []
        for i in range(self.model.rowCount()):
            if self.model.item(i).checkState():
                index = i + 1
                lsd.append(index)
        print (lsd)
                
app = QApplication(sys.argv)
tsk = MyLoadTskList()
tsk.show()
app.exec_()
