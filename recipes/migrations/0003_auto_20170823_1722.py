# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-08-23 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20170823_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='dish_type',
            field=models.CharField(choices=[('VEG', 'VEGETABLE'), ('MEA', 'MEAT'), ('CAR', 'CARBOHYDRATE'), ('ALL', 'ALL-IN-ONE'), ('OTH', 'OTHER')], default='VEG', max_length=3),
        ),
    ]
