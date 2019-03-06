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
    'projectPath' : '' 
}

def getProjectPath():
    if os.path.exists(configPath): # 判断文件是否存在
        f = open(configPath, 'r')
        try:
            data = json.loads(f.read())
            if os.path.exists(data['projectPath']):
                return data['projectPath']
        except Exception as e:
            print('DefaultConfigure error')

def setProjectPath(path):
    if os.path.exists(path):
        pathInfo['projectPath'] = path
        f = open(configPath, 'w')
        f.write(json.dumps(pathInfo)) 


if __name__ == '__main__':
    print(getProjectPath())
    setProjectPath("E:\\2019\\AM_Test")