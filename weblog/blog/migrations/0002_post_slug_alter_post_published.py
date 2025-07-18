# Generated by Django 5.2.3 on 2025-07-15 15:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2025, 7, 15, 15, 7, 42, 216220, tzinfo=datetime.timezone.utc)),
        ),
    ]
