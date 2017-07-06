from django.db import models


class userinfo(models.Model):
    user_name = models.CharField(max_length=20)
    user_pwd = models.CharField(max_length=40)
    user_email = models.CharField(default='', max_length=30)
    user_phone = models.CharField(default='', max_length=11)
    recv_name = models.CharField(default='', max_length=20)
    user_addr = models.CharField(default='', max_length=100)
    post_code = models.CharField(default='', max_length=6)

