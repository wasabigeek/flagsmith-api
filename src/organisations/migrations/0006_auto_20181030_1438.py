# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-30 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0005_auto_20181025_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='plan',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='subscription_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='SubscriptionDate'),
        ),
    ]
