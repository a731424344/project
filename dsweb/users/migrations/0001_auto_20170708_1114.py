# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '01userinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='post_code',
            field=models.CharField(default=b'', max_length=6),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='recv_name',
            field=models.CharField(default=b'', max_length=20),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_addr',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_email',
            field=models.CharField(default=b'', max_length=30),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user_phone',
            field=models.CharField(default=b'', max_length=11),
        ),
    ]
