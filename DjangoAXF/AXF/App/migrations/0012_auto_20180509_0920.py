# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-09 01:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(upload_to=''),
        ),
    ]
