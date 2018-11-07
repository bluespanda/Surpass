# -*- coding: utf-8 -*-
"""
    Surpass:dbutils
    数据库管理工具类
    用于数据库创建，数据库用户管理等
    本文件的运行依赖于PyMySQL，运行前请确保PyMySQL已经安装
    :copyright: (c) 2018 by Surpass.
    :license: GPLv2, see LICENSE File for more details.
"""

import pymysql as PyMySQL


def cre_db(host, user, pw, name):
    try:
        # 数据库连接
        db = PyMySQL.connect(host, user, pw, charset='utf8')
        # 创建游标，通过连接与数据通信
        cursor = db.cursor()
        # 执行sql语句
        cursor.execute('show databases')
        rows = cursor.fetchall()
        for row in rows:
            tmp = "%2s" % row
            print(row[0])
            print(tmp)
    except PyMySQL.Error as e:
        print('Mysql Error %d: %s') % (e.args[0], e.args[1])
    finally:
        # 关闭数据库连接
        db.close()


def get_all_dbs(ip, port, user, password, charset):
    data = []
    try:
        db = PyMySQL.connect(host=ip, port=port, user=user, passwd=password, charset=charset)
        cursor = db.cursor()
        cursor.execute('show databases')
        rows = cursor.fetchall()
        for row in rows:
            data.append(row[0])
    except PyMySQL.Error as e:
        print('Mysql Error %d: %s') % (e.args[0], e.args[1])
    finally:
        if db is not None:
            db.close()
        return data


def get_all_users(ip, port, username, password, charset):
    data = [];
    try:
        db = PyMySQL.connect(host=ip, port=port, user=username, passwd=password, charset=charset)
        cursor = db.cursor()
        cursor.execute('select user,host from mysql.user')
        rows = cursor.fetchall()
        for row in rows:
            data.append(row[0])
    except PyMySQL.Error as e:
        print('Mysql Error %d: %s') % (e.args[0], e.args[1])
    finally:
        if db is not None:
            db.close()
        return data
