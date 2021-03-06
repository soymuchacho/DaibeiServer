# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-19 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_id', models.CharField(max_length=256)),
                ('resource_name', models.CharField(max_length=256)),
                ('resource_path', models.CharField(max_length=256)),
                ('resource_size', models.IntegerField()),
                ('resource_type', models.IntegerField()),
                ('resource_describe', models.CharField(max_length=1024)),
            ],
        ),
    ]
