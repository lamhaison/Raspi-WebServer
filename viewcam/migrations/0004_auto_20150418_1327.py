# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewcam', '0003_auto_20150411_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videooption',
            name='default',
            field=models.BooleanField(default=False, verbose_name=b'Set default Value'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='videooption',
            name='type',
            field=models.CharField(max_length=50, verbose_name=b'Parameter Types', choices=[(b'bitrate', b'Bitrate'), (b'fps', b'Frame per second'), (b'size', b'Size')]),
            preserve_default=True,
        ),
    ]
