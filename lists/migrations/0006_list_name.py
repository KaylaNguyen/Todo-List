# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_item_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='name',
            field=models.TextField(default=''),
        ),
    ]
