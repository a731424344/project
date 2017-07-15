from django.db import models

# Create your models here.

class OrderMain(models.Model):
    order_id = models.CharField(max_length=30,primary_key=True)
    user = models.ForeignKey('users.userinfo')
    order_date = models.DateTimeField(auto_now_add= True)
    total = models.DecimalField(max_digits=9,decimal_places=2,default=0)
    state = models.IntegerField(default=0)

class OrderDetail(models.Model):
    price = models.DecimalField(max_digits=6,decimal_places=2)
    count = models.IntegerField(default=0)
    order = models.ForeignKey('OrderMain')
    goods = models.ForeignKey('Goods.GoodsInfo')


