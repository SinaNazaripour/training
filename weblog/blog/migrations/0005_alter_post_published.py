# Generated by Django 5.2.3 on 2025-07-17 14:48

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_published_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published',
            field=django_jalali.db.models.jDateTimeField(default=datetime.datetime(2025, 7, 17, 14, 48, 19, 228608, tzinfo=datetime.timezone.utc)),
        ),
    ]
