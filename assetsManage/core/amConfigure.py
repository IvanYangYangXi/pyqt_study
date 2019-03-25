#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# amConfigure.py
# @Author : Ivan-杨杨兮 (523166477@qq.com)
# @Link   : www.cgartech.com
# @Date   : 2019/3/4 下午11:05:47


import os
import json

configPath = os.path.dirname(os.path.dirname(__file__)) + '/config/DefaultConfigure.json'

pathInfo = {
    'projectPath' : '',
    'collectionPath' : []
}


def loadConfig():
    if os.path.exists(configPath): # 判断文件是否存在
        f = open(configPath, 'r')
        try:
            data = json.loads(f.read())
            f.close()
            return data
        except Exception as e:
            f.close()
            print('DefaultConfigure error:%s'%(e))

# ------------ 工程目录 --------------------- #
def getProjectPath():
    try:
        data = loadConfig()
        if os.path.exists(data['projectPath']):
            return data['projectPath']
    except Exception as e:
        print('DefaultConfigure error')

def setProjectPath(path):
    if os.path.exists(path):
        data = loadConfig()
        data['projectPath'] = path
        f = open(configPath, 'w')
        f.write(json.dumps(data)) 

# ------------ 搜藏目录 --------------------- #
def getCollectionPath():
    if os.path.exists(configPath): # 判断文件是否存在
        f = open(configPath, 'r')
        try:
            data = json.loads(f.read())
            return data['collectionPath']
        except Exception as e:
            print('DefaultConfigure error')

def addCollectionPath(path):
    if os.path.exists(path):
        data = loadConfig()
        if not path in data['collectionPath']:
            data['collectionPath'].append(path)
            f = open(configPath, 'w')
            f.write(json.dumps(data)) 

def removeCollectionPath(path):
    data = loadConfig()
    if path in data['collectionPath']:
        data['collectionPath'].remove(path)
        f = open(configPath, 'w')
        f.write(json.dumps(data)) 


if __name__ == '__main__':
    print(getProjectPath())
    setProjectPath("E:\\2019\\AM_Test")