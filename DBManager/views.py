from django.shortcuts import render

from . import dbutils
from . import models
from Surpass.utils import JsonHelper


# Create your views here.
def index(request):
    return render(request, "db/index.html")


def host_list(request):
    is_json = request.GET.get("is_json")
    hosts = models.Host.objects.all()
    if is_json is "1":
        return render(request, "toJson.html", {'DATA': JsonHelper.toJSON(hosts, 1, 1, hosts.count())})
    else:
        return render(request, "hosts/index.html", {'hosts': hosts})


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
    root_password = request.POST.get('rootpwd')
    root = request.POST.get("root")
    ip = request.POST.get("ip")
    name = request.POST.get('name')
    host_id = request.POST.get('host_id', '0')
    port = request.POST.get("port", "3306")
    if host_id == '0':
        models.Host.objects.create(name=name, ip=ip, root=root, rootpwd=root_password, port=port)
    else:
        host = models.Host.objects.get(pk=host_id)
        host.name = name
        host.ip = ip
        host.root = root
        host.rootpwd = root_password
        # host.read = read
        # host.readpwd = readpwd
        host.port = port
        host.save()
    hosts = models.Host.objects.all()
    return render(request, "hosts/index.html", {'hosts': hosts})


def database_list(request):
    hosts = models.Host.objects.all()
    return render(request, "databases/hosts.html", {'DATA': hosts})


def databases_for_host(request, host_id):
    if str(host_id) == '0':
        return render(request, "404.html", {'return_url': "/", "error_msg": "相关请求数据错误！"})
    host = models.Host.objects.get(pk=host_id)
    data = dbutils.get_all_dbs(host.ip, int(host.port), host.root, host.rootpwd, "utf8")
    return render(request, "toJson.html", {'DATA': JsonHelper.toJSON(data, 1, 1, len(data))})


def databases(request):
    databaselist = models.Database.objects.all()
    return render(request, "databases/index.html", {'databaselist': databaselist})


def database_edit_page(request, database_id):
    if str(database_id) == '0':
        return render(request, "databases/edit_page.html")
    database = models.Database.objects.get(pk=database_id)
    return render(request, "databases/edit_page.html", {'database': database})


def database_edit_action(request):
    databasename = request.POST.get('databaseName')
    dbcharSet = request.POST.get('dbcharSet', 'utf-8')
    database_id = request.POST.get('database_id', '0')
    if database_id == '0':
        models.Database.objects.create(databaseName=databasename, dbcharSet=dbcharSet)
        # 保存完后还要完成创建数据库的操作

    else:
        database = models.Database.objects.get(pk=database_id)
        database.databaseName = databasename
        database.dbcharSet = dbcharSet
        database.save()
        # 保存完后还要完成创建数据库的操作

    odatabases = models.Database.objects.all()
    return render(request, "databases/index.html", {'databases': odatabases})


def database_delete_page(request, database_id):
    if str(database_id) != '0':
        database = models.Database.objects.get(pk=database_id)
        database.delete()
        # 删除数据库中对象后要完成相应数据库的删除操作
    odatabases = models.Database.objects.all()
    return render(request, "databases/index.html", {'databases': odatabases})
