# Generated by Django 3.2.25 on 2024-07-10 19:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20240710_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='ical_links',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, default=list, size=None),
        ),
    ]
