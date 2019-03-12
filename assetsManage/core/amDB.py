#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# AM_db.py
# @Author : Ivan-杨杨兮 (523166477@qq.com)
# @Link   : www.cgartech.com
# @Date   : 2019/3/2 上午10:27:25


import sqlite3
import os
import re


# 建立自增主键:id integer primary key autoincrement
table_list = '''list(
    id integer primary key autoincrement,
    listName CHAR(30),
    listComplete bool,
    itemNames text,
    itemCompletes text
)'''
struct_list = '''
    listName, 
    listComplete, 
    itemNames, 
    itemCompletes
'''

table_assets = '''assets(
    id integer primary key autoincrement,
    name NCHAR(50),
    local NVARCHAR(500),
    type CHAR(30),
    state int,
    label text,
    dueDate CHAR(30),
    reporter NCHAR(30),
    describe text,
    comment text,
    img text,
    video text,
    tasklist int,
    FOREIGN KEY (tasklist) REFERENCES list(id)
)'''
struct_assets = '''
    name, 
    local,
    type, 
    state, 
    label,
    dueDate,
    reporter,
    describe,
    comment,
    img,
    video,
    tasklist
'''

amdbPath = os.path.dirname(os.path.dirname(__file__)) + '/data/amdb.db'


# 执行操作
def executeDB(query):
    conn = sqlite3.connect(amdbPath) # 连接数据库
    conn.text_factory = str
    cursor = conn.cursor()

    result = cursor.execute(query) # 执行操作
    students = result.fetchall()

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接
    return students

# 执行多次操作
def executemanyDB(query, data):
    conn = sqlite3.connect(amdbPath) # 连接数据库
    conn.text_factory = str
    cursor = conn.cursor()

    result = cursor.executemany(query, data) # 执行多次操作
    students = result.fetchall()

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接
    return students


# 创建sqlite3数据表
def CreateTable():
    conn = sqlite3.connect(amdbPath) # 连接数据库
    conn.text_factory = str
    
    conn.execute("create table IF NOT EXISTS " + table_list) # 执行操作
    conn.execute("create table IF NOT EXISTS " + table_assets) # 执行操作

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

# 重新创建数据表
def reCreateTable(tableName):
    conn = sqlite3.connect(amdbPath) # 连接数据库
    conn.text_factory = str
    
    conn.execute("drop table IF EXISTS %s"%(tableName)) # 删除表

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

    CreateTable() # 创建表

# 插入
def insertData(tableName, tableStruct, data):
    conn = sqlite3.connect(amdbPath) # 连接数据库
    conn.text_factory = str
    try:
        conn.execute("insert into " + tableName + "(" + tableStruct + \
            ")" + "VALUES (?%s)"%(',?'*(len(re.findall(r',', tableStruct)))), data) # 执行操作
    except Exception as e:
        print(e)
    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

# 插入多个
def insertManyData(tableName, tableStruct, datas):
    conn = sqlite3.connect(amdbPath) # 连接数据库
    conn.text_factory = str
    try:
        conn.executemany("insert into " + tableName + "(" + tableStruct + \
            ")" + "VALUES (?%s)"%(',?'*(len(re.findall(r',', tableStruct)))), datas) # 执行操作
    except Exception as e:
        print(e)
    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

# 查询数据
def findData(tableName, theData, keys=''):
    conn = sqlite3.connect(amdbPath) # 连接数据库
    cursor = conn.cursor()

    if keys == '':
        result = cursor.execute('SELECT * FROM ' + tableName + ' WHERE ' + theData) # 执行操作
    else:
        result = cursor.execute('SELECT ' + keys + ' FROM ' + tableName + ' WHERE ' + theData) # 执行操作
    student = result.fetchone()

    # conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接
    return student
    
# 查询数据（返回列表）
def findDatas(tableName, theData, keys=''):
    conn = sqlite3.connect(amdbPath) # 连接数据库
    cursor = conn.cursor()

    if keys == '':
        result = cursor.execute('SELECT * FROM ' + tableName + ' WHERE ' + theData) # 执行操作
    else:
        result = cursor.execute('SELECT ' + keys + ' FROM ' + tableName + ' WHERE ' + theData) # 执行操作
    students = result.fetchall()

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接
    return students

# 遍历数据（返回列表）
def getDatas(tableName, keys=''):
    conn = sqlite3.connect(amdbPath) # 连接数据库
    cursor = conn.cursor()

    if keys == '':
        result = cursor.execute('SELECT * FROM ' + tableName) # 执行操作
    else:
        result = cursor.execute('SELECT ' + keys + ' FROM ' + tableName) # 执行操作
    students = result.fetchall()

    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接
    return students

# 删除数据
def deleteData(tableName, theData):
    conn = sqlite3.connect(amdbPath) # 连接数据库
    try:
        conn.execute('DELETE FROM ' + tableName + ' WHERE ' + theData) # 执行操作
    except Exception as e:
        print(e)
    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接

# 修改数据
def updateData(tableName, theData, newData):
    conn = sqlite3.connect(amdbPath) # 连接数据库
    try:
        conn.execute('UPDATE ' + tableName + ' SET ' + newData + ' WHERE ' + theData) # 执行操作
    except Exception as e:
        print(e)
    conn.commit() # 保存修改
    conn.close() # 关闭与数据库的连接


if __name__ == '__main__':
    # CreateTable()
    reCreateTable('list')
    reCreateTable('assets')
    insertData('list', struct_list, ('nnn', False, 'aaa', 'bbb'))
    insertData('list', struct_list, ('n11', False, 'aaa', 'bbb'))
    insertData('list', struct_list, ('n22', False, 'aaa', 'bbb'))
    updateData('list', 'listName="n11"', 'listName="g11",listComplete=1')
    deleteData('list', 'listName="n22"')
    print(findData('list', "listName='g11'")[0])
    print(findData('list', "listName='g11'", 'listName'))