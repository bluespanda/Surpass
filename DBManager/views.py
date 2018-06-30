from django.shortcuts import render
from . import models
from Surpass.utils import JsonHelper


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
    readpwd = request.POST.get('readpwd')
    read = request.POST.get('read')
    rootpwd = request.POST.get('rootpwd')
    root = request.POST.get("root")
    ip = request.POST.get("ip")
    name = request.POST.get('name')
    host_id = request.POST.get('host_id', '0')
    if host_id == '0':
        models.Host.objects.create(name=name, ip=ip, root=root, rootpwd=rootpwd, read=read, readpwd=readpwd)
    else:
        host = models.Host.objects.get(pk=host_id)
        host.name = name
        host.ip = ip
        host.root = root
        host.rootpwd = rootpwd
        host.read = read
        host.readpwd = readpwd
        host.save()
    hosts = models.Host.objects.all()
    return render(request, "hosts/index.html", {'hosts': hosts})
