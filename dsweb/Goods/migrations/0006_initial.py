# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_auto_20170708_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('com_date', models.DateTimeField(default=b'')),
                ('com_pid', models.IntegerField(default=-1)),
                ('com_content', models.CharField(max_length=400)),
                ('isDelete', models.BooleanField(default=0)),
                ('com_zan', models.IntegerField(default=0)),
                ('com_reply', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gtitle', models.CharField(max_length=60)),
                ('gpic', models.ImageField(upload_to=b'goods/')),
                ('gprice', models.DecimalField(max_digits=6, decimal_places=2)),
                ('gclick', models.IntegerField(default=0)),
                ('gunit', models.CharField(max_length=30)),
                ('isDelete', models.BooleanField(default=False)),
                ('gsubtitle', models.CharField(max_length=230)),
                ('grepertory', models.IntegerField(default=100)),
                ('gdetails', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ttitle', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gtype',
            field=models.ForeignKey(to='Goods.TypeInfo'),
        ),
        migrations.AddField(
            model_name='goodscomment',
            name='com_type',
            field=models.ForeignKey(to='Goods.GoodsInfo'),
        ),
        migrations.AddField(
            model_name='goodscomment',
            name='com_user',
            field=models.ForeignKey(to='users.userinfo'),
        ),
    ]
