import datetime
import json

from django.db import models

# Create your models here.


class Host(models.Model):
    name = models.CharField(max_length=255, null=False)
    ip = models.CharField(max_length=255, null=False)
    cpu = models.CharField(max_length=255)
    mem = models.CharField(max_length=255)
    disk = models.CharField(max_length=255)
    idc = models.CharField(max_length=255)
    rootpwd = models.CharField(max_length=255, null=False)
    readpwd = models.CharField(max_length=255, null=False)
    group = models.CharField(max_length=255)
    createdTime = models.DateTimeField(auto_now_add=True)
    root = models.CharField(max_length=255, null=False)
    read = models.CharField(max_length=255, null=False)
    comment = models.TextField()

    class Meta:
        db_table = 'dbmanager_host'

    def __str__(self):
        return str(self.id) + " - " + self.name + " - " + self.ip

    def getfield(self):
        field = [f.name for f in self._meta.fields]
        field.remove('rootpwd')
        field.remove('readpwd')
        return field

    def get_json(self):
        field = self.getfield()
        result = {}
        for attr in field:
            if isinstance(getattr(self, attr), datetime.datetime):
                result[str(attr).upper()] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                result[str(attr).upper()] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                result[str(attr).upper()] = getattr(self, attr)
        return json.dumps(result)
