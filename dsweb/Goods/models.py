# -*- coding:utf-8 -*-
from django.db import models
from tinymce.models import HTMLField


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.ttitle.encode('utf-8')


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=60)
    gpic = models.ImageField(upload_to='goods/')
    gprice = models.DecimalField(max_digits=6,decimal_places=2)
    gclick = models.IntegerField(default=0)
    gunit = models.CharField(max_length=30)
    isDelete = models.BooleanField(default=False)
    gsubtitle = models.CharField(max_length=230)
    grepertory = models.IntegerField(default=100)
    gdetails = HTMLField()
    gtype = models.ForeignKey('TypeInfo')



class GoodsComment(models.Model):
    com_type = models.ForeignKey('GoodsInfo')
    com_user = models.ForeignKey('users.userinfo')
    com_date = models.DateTimeField(default='')
    com_pid = models.IntegerField(default= -1)
    com_content = models.CharField(max_length=400)
    isDelete = models.BooleanField(default=0)
    com_zan = models.IntegerField(default=0)
    com_reply = models.CharField(max_length=200)

