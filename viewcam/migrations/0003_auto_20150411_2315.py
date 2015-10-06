# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewcam', '0002_auto_20150411_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='videooption',
            name='default',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='videooption',
            name='type',
            field=models.CharField(max_length=50, verbose_name=b'Parameter Types'),
            preserve_default=True,
        ),
    ]
