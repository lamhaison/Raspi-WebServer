# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewcam', '0001_initial'),
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
                ('dev', models.ForeignKey(to='viewcam.Device')),
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
                ('dev', models.ForeignKey(to='viewcam.Device')),
            ],
            options={
                'db_table': 'alarmtime',
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
            name='VideoOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.CharField(max_length=50, verbose_name=b'Description')),
                ('type', models.CharField(max_length=50, verbose_name=b'Kind of Option')),
                ('value', models.CharField(max_length=50, verbose_name=b'Value')),
            ],
            options={
                'db_table': 'video_option',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='alerttemp',
            name='dev',
        ),
        migrations.DeleteModel(
            name='AlertTemp',
        ),
        migrations.RemoveField(
            model_name='alerttime',
            name='dev',
        ),
        migrations.DeleteModel(
            name='AlertTime',
        ),
        migrations.AddField(
            model_name='device',
            name='status',
            field=models.CharField(default=b'OFF', max_length=5),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='temperature',
            name='type',
            field=models.CharField(default=b'1m', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='id',
            field=models.IntegerField(serialize=False, verbose_name=b'Pin', primary_key=True),
            preserve_default=True,
        ),
    ]
