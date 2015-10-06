# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlarmTemp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=3, null=True, blank=True)),
                ('condition', models.CharField(max_length=8, null=True, blank=True)),
                ('value', models.FloatField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
                ('true_count', models.IntegerField(default=0)),
                ('false_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'alarmtemp',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AlarmTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action', models.CharField(max_length=3, null=True, blank=True)),
                ('time', models.DateTimeField(null=True, blank=True)),
                ('timer', models.IntegerField(null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'alarmtime',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.IntegerField(serialize=False, verbose_name=b'Pin', primary_key=True)),
                ('dev_name', models.CharField(unique=True, max_length=10)),
                ('desc', models.CharField(max_length=50, null=True, blank=True)),
                ('status', models.CharField(default=b'OFF', max_length=5)),
            ],
            options={
                'db_table': 'devices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeviceHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('from_status', models.CharField(default=b'ON', max_length=5)),
                ('to_status', models.CharField(default=b'OFF', max_length=5)),
                ('dev', models.ForeignKey(to='viewcam.Device')),
            ],
            options={
                'db_table': 'history',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('value', models.FloatField()),
                ('type', models.CharField(default=b'1m', max_length=10)),
            ],
            options={
                'db_table': 'temp',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VideoOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.CharField(max_length=50, verbose_name=b'Description')),
                ('type', models.CharField(max_length=50, verbose_name=b'Parameter Types', choices=[(b'bitrate', b'Bitrate'), (b'fps', b'Frame per second'), (b'size', b'Size')])),
                ('value', models.CharField(max_length=50, verbose_name=b'Value')),
                ('default', models.BooleanField(default=False, verbose_name=b'Set default Value')),
            ],
            options={
                'db_table': 'video_option',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='alarmtime',
            name='dev',
            field=models.ForeignKey(to='viewcam.Device'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alarmtemp',
            name='dev',
            field=models.ForeignKey(to='viewcam.Device'),
            preserve_default=True,
        ),
    ]
