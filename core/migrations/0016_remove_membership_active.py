# Generated by Django 3.2.25 on 2024-07-26 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20240725_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='active',
        ),
    ]
