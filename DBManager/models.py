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
    createdTime = models.DateField(auto_now_add=True)
    root = models.CharField(max_length=255, null=False)
    read = models.CharField(max_length=255, null=False)
    comment = models.TextField()

    def __str__(self):
        return str(self.id) + " - " + self.name + " - " + self.ip
