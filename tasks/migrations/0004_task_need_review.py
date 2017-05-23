# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_frozen'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='need_review',
            field=models.BooleanField(default=False),
        ),
    ]
