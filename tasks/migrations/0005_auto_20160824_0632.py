# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_task_need_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='ticket_id',
            field=models.IntegerField(unique=True),
        ),
    ]
