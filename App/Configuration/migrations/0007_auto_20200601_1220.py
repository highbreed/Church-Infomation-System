# Generated by Django 3.0.6 on 2020-06-01 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Configuration', '0006_auto_20200601_1152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='phone_number',
            new_name='contact',
        ),
    ]
