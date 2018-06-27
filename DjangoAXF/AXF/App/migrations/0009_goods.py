# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-07 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_foodtype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.CharField(max_length=20)),
                ('productimg', models.CharField(max_length=200)),
                ('productname', models.CharField(max_length=20)),
                ('productlongname', models.CharField(max_length=200)),
                ('isxf', models.BooleanField(default=0)),
                ('pmdesc', models.CharField(max_length=200)),
                ('specifics', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('marketprice', models.FloatField()),
                ('categoryid', models.CharField(max_length=20)),
                ('childcid', models.CharField(max_length=20)),
                ('childcidname', models.CharField(max_length=20)),
                ('dealerid', models.CharField(max_length=20)),
                ('storenums', models.IntegerField(default=1)),
                ('productnum', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'axf_goods',
            },
        ),
    ]