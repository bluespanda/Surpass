# -*- coding: utf-8 -*-
import datetime

from django.db.models.query import QuerySet
import json
from django.db import models

"""
    Surpass:utils
    用于一些工具类操作
    :copyright: (c) 2018 by Surpass.
    :license: GPLv2, see LICENSE File for more details.
"""


class JsonHelper:
    """
    功能：
        用于对数据进行转换成JSON串
    说明：

    作者：
        Jack Chu:chuchuanbao@gmail.com
    日期：
        2018/6/30
    """

    @classmethod
    def toJSON(cls, obj, pagesize=0, pageindex=0, count=0):
        if obj is None:
            return "{}"
        elif isinstance(obj, models.Model):
            return obj.get_json()
        elif isinstance(obj, QuerySet):
            data = []
            if pageindex <= 0 or pagesize <= 0:
                for o in obj:
                    data.append(json.loads(JsonHelper.toJSON(o)))
                return json.dumps(data)
            else:
                if count <= 0:
                    data = []
                else:
                    for i in range(pagesize * (pageindex - 1), pagesize * pageindex):
                        if obj[i] is None:
                            break
                        else:
                            data.append(json.loads(JsonHelper.toJSON(obj[i])))
                result = {'DATA': data, 'PAGER': JsonHelper.genePager(pagesize, pageindex, count)}
                return json.dumps(result)
        else:
            result = {}
            for attr in [f.name for f in obj._meta.fields]:
                if isinstance(getattr(obj, attr), datetime.datetime):
                    result[str(attr).upper()] = getattr(obj, attr).strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(getattr(obj, attr), datetime.date):
                    result[str(attr).upper()] = getattr(obj, attr).strftime('%Y-%m-%d')
                else:
                    result[str(attr).upper()] = getattr(obj, attr)
            return json.dumps(result)

    @classmethod
    def genePager(cls, pagesize=0, pageindex=0, count=0):
        if count > 0:
            if count % pagesize == 0:
                pagecount = count / pagesize
            else:
                pagecount = count / pagesize + 1
        else:
            pagecount = 0
        return {'PAGESIZE': pagesize, 'PAGEINDEX': pageindex, 'COUNT': count, 'PAGECOUNT': pagecount}
