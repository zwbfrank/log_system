# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-26 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0003_log_userinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]