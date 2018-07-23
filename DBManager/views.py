from django.shortcuts import render

from DBManager.dbutils import cre_db
from . import models
from Surpass.utils import JsonHelper
from Surpass.utils import StringUtils


# Create your views here.
def index(request):
    return render(request, "db/index.html")


def host_list(request):
    hosts = models.Host.objects.all()
    return render(request, "toJson.html", {'DATA': JsonHelper.toJSON(hosts, 1, 1, hosts.count())})


def host_detail(request, host_id):
    host = models.Host.objects.get(pk=host_id)
    return render(request, "toJson.html", {'DATA': JsonHelper.toJSON(host)})


def host_edit_page(request, host_id):
    if str(host_id) == '0':
        return render(request, "hosts/edit_page.html")
    host = models.Host.objects.get(pk=host_id)
    return render(request, "hosts/edit_page.html", {'host': host})


def host_delete(request, host_id):
    if str(host_id) != "0":
        host = models.Host.objects.get(pk=host_id)
        host.delete()
    hosts = models.Host.objects.all()
    return render(request, "hosts/index.html", {'hosts': hosts})


def host_edit_action(request):
    host_id = request.POST.get('host_id', '0')
    name = request.POST.get('name')
    ip = request.POST.get("ip")
    port = request.POST.get("port")
    username = request.POST.get("username")
    password = request.POST.get("password")
    if host_id == '0':
        models.Host.objects.create(name=name, ip=ip, port=port, username=username, password=password)
    else:
        host = models.Host.objects.get(pk=host_id)
        host.name = name
        host.ip = ip
        host.port = port
        host.username = username
        host.password = password
        host.save()
    hosts = models.Host.objects.all()
    return render(request, "hosts/index.html", {'hosts': hosts})


def database_list(request):
    databases = models.Database.objects.all()
    return render(request, "toJson.html", {'DATA': JsonHelper.toJSON(databases, 1, 1, databases.count())})


def databases(request):
    databaselist = models.Database.objects.all()
    return render(request, "databases/index.html", {'databaselist': databaselist})


def database_edit_page(request, database_id):
    if str(database_id) == '0':
        return render(request, "databases/edit_page.html")
    database = models.Database.objects.get(pk=database_id)
    return render(request, "databases/edit_page.html", {'database': database})


def database_edit_action(request):
    # 正确的创建数据库的步骤不应该是这样的应该是先有一步，连接数据库成功后，在已有连接上进行数据库的创建#
    host = request.POST.get('host')
    username = request.POST.get('username')
    password = request.POST.get('password')
    databasename = request.POST.get('databaseName')
    dbcharSet = request.POST.get('dbcharSet', 'utf-8')
    database_id = request.POST.get('database_id', '0')
    if database_id == '0':
        models.Database.objects.create(databaseName=databasename, dbcharSet=dbcharSet)
        # 保存完后还要完成创建数据库的操作
        cre_db(host, username, password, databasename)
    else:
        database = models.Database.objects.get(pk=database_id)
        database.databaseName = databasename
        database.dbcharSet = dbcharSet
        database.save()
        # 保存完后还要完成创建数据库的操作
        cre_db(host, username, password, databasename)
    odatabases = models.Database.objects.all()
    return render(request, "databases/index.html", {'databases': odatabases})


def database_delete_page(request, database_id):
    if str(database_id) != '0':
        database = models.Database.objects.get(pk=database_id)
        database.delete()
        # 删除数据库中对象后要完成相应数据库的删除操作
    odatabases = models.Database.objects.all()
    return render(request, "databases/index.html", {'databases': odatabases})


def db_user_lists(request, host_id):
    if StringUtils.is_empty(host_id) or int(host_id) < 1:
        return render(request, "error.html", {"ERROR": {"MSG": "相关主机不存在"}})
    else:
        try:
            host = models.Host.objects.get(pk=host_id)
            sql = "select Host,User from mysql.user;"
            import pymysql
            db = pymysql.connect(host=host.ip, user=host.username, password=host.password, database='mysql',
                                 port=host.port, unix_socket=None, charset='utf8')
            cursor = db.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            user_lists = []
            for row in rows:
                user = {
                    "Host": row[0],
                    "User": row[1]
                }
                user_lists.append(user)
            return render(request, "toJson.html", {'DATA': JsonHelper.toJSON(user_lists, 0, 0, len(user_lists))})
        except Exception as e:
            print(e.args)
            return render(request, "error.html", {"ERROR": {"MSG": "相关主机不存在"}})
