#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# spinbox_test1.py
# @Author :  ()
# @Link   : 
# @Date   : 2/13/2019, 9:26:06 AM


from PySide2 import QtWidgets, QtCore, QtUiTools


def loadui(uiPath):
    uiFile = QtCore.QFile(uiPath)
    uiFile.open(QtCore.QFile.ReadOnly)
    uiWindow = QtUiTools.QUiLoader().load(uiFile)
    uiFile.close()
    return uiWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, uiPath='', parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = loadui(uiPath)
        self.ui.show()
    


if __name__ == '__main__':
    mainWindow = MainWindow()