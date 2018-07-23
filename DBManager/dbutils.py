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

db_host = ''
db_user = ''
db_pw = ''
db_name = 'vdt'


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
            # 判断数据库是否存在
            if name == tmp:
                cursor.execute('drop database if exists ' + name)
                cursor.execute('create database if not exists ' + name)
                # 提交到数据库执行
                db.commit()
    except PyMySQL.Error as e:
        print('Mysql Error %d: %s') % (e.args[0], e.args[1])
    finally:
        # 关闭数据库连接
        db.close()


# cre_db(db_host, db_user, db_pw)
