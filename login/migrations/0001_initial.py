# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('userid', models.IntegerField()),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=320)),
                ('phone', models.CharField(max_length=64)),
                ('position', models.IntegerField()),
                ('birthday', models.CharField(max_length=64)),
                ('sex', models.IntegerField()),
                ('number', models.CharField(max_length=64)),
                ('manager', models.CharField(max_length=64)),
                ('entry_time', models.CharField(max_length=64)),
            ],
        ),
    ]
