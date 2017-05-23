# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20160824_0632'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='review_time',
            field=models.FloatField(default=0),
        ),
    ]
