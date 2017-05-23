# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='iteration',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['ordering']},
        ),
        migrations.AddField(
            model_name='task',
            name='ordering',
            field=models.IntegerField(default=0),
        ),
    ]
