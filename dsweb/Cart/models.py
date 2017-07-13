# -*- coding:utf-8 -*-
from django.db import models

class CartInfo(models.Model):
    user = models.ForeignKey('users.userinfo')
    goods = models.ForeignKey('Goods.GoodsInfo')
    count = models.IntegerField()

