# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket_id', models.IntegerField()),
                ('summary', models.CharField(max_length=512)),
                ('estimated_hours', models.FloatField(default=0)),
                ('iteration', models.ForeignKey(to='tasks.Iteration')),
                ('owner', models.ForeignKey(blank=True, to='tasks.Member', null=True)),
            ],
        ),
    ]
