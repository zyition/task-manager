# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_task_review_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='iteration',
            name='planned_time',
            field=models.FloatField(default=0),
        ),
    ]
