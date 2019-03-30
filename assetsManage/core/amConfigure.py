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

defaultConfig = {
    'lastProject' : 'DefaultProject',
    'DefaultProject' : {
        'projectPath' : '',
        'branch' : '',
        'collectionPath' : []
    }  
}

# 读取配置文件信息
def loadConfig():
    if os.path.exists(configPath): # 判断文件是否存在
        f = open(configPath, 'r')
        try:
            data = json.loads(f.read())
            f.close()
            return data
        except Exception as e:
            f.close()
            print('DefaultConfigure error:%s:%e%s'%(e))

# 获取最后一次打开的工程名称
def getLastProjectName():
    try:
        data = loadConfig()
        if ('lastProject' in data.keys()): # 判断字典是否存在某个key
            if (data['lastProject'] in data.keys()):
                return data['lastProject']
            else:
                f = open(configPath, 'w')
                f.write(json.dumps(data)) 
                return 'DefaultProject'
        else:
            f = open(configPath, 'w')
            f.write(json.dumps(defaultConfig)) 
            return 'DefaultProject'
    except Exception as e:
        f = open(configPath, 'w')
        f.write(json.dumps(defaultConfig)) 
        return 'DefaultProject'
        print('lastProject error')

# 设置最后一次打开的工程名称
def setLastProjectName(name):
    data = loadConfig()
    data['lastProject'] = name
    f = open(configPath, 'w')
    f.write(json.dumps(data)) 

# 添加新工程
def addNewProject(name, path):
    data = loadConfig()
    if not (name in data.keys()):
        data[name] = {
            'projectPath' : path,
            'collectionPath' : []
        }
        data['lastProject'] = name
        f = open(configPath, 'w')
        f.write(json.dumps(data)) 
        return True
    else:
        return False

# 移除工程
def removeProject(name):
    data = loadConfig()
    if (name in data.keys()):
        del data[name]

# ------------ 工程目录 --------------------- #
def getProjectPath():
    try:
        data = loadConfig()
        if os.path.isdir(data[getLastProjectName()]['projectPath']):
            return data[getLastProjectName()]['projectPath']
        else:
            return ''
    except Exception as e:
        print('DefaultConfigure error:%s'%e)

def setProjectPath(path):
    if os.path.exists(path):
        try:
            data = loadConfig()
            data[getLastProjectName()]['projectPath'] = path
            f = open(configPath, 'w')
            f.write(json.dumps(data)) 
        except Exception as e:
            print('DefaultConfigure error:%s'%e)

# ------------ 分支 ---------------- #
def getProjectBranch():
    try:
        data = loadConfig()
        return data[getLastProjectName()]['branch']
    except Exception as e:
        data = loadConfig()
        data[getLastProjectName()]['branch'] = ''
        f = open(configPath, 'w')
        f.write(json.dumps(data)) 
        print('DefaultConfigure error:%s'%e)
        return ''

def setProjectBranch(branch):
    try:
        data = loadConfig()
        data[getLastProjectName()]['branch'] = branch
        f = open(configPath, 'w')
        f.write(json.dumps(data)) 
    except Exception as e:
        print('DefaultConfigure error:%s'%e)

# ------------ 搜藏目录 --------------------- #
def getCollectionPath():
    if os.path.exists(configPath): # 判断文件是否存在
        f = open(configPath, 'r')
        try:
            data = loadConfig()
            return data[getLastProjectName()]['collectionPath']
        except Exception as e:
            print('DefaultConfigure error:%s'%e)

def addCollectionPath(path):
    if os.path.exists(path):
        data = loadConfig()
        if not path in data[getLastProjectName()]['collectionPath']:
            data[getLastProjectName()]['collectionPath'].append(path)
            f = open(configPath, 'w')
            f.write(json.dumps(data)) 

def removeCollectionPath(path):
    data = loadConfig()
    if path in data[getLastProjectName()]['collectionPath']:
        data[getLastProjectName()]['collectionPath'].remove(path)
        f = open(configPath, 'w')
        f.write(json.dumps(data)) 


if __name__ == '__main__':
    print(getProjectPath())
    setProjectPath("E:\\2019\\AM_Test")