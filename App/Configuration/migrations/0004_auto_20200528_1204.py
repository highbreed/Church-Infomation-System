# Generated by Django 3.0.6 on 2020-05-28 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Configuration', '0003_auto_20200528_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemuser',
            name='role',
            field=models.CharField(choices=[('ChairPerson', 'ChairPerson'), ('Secretary', 'Secretary'), ('Treasurer', 'Treasurer')], max_length=12),
        ),
    ]
