# Generated by Django 3.0.6 on 2020-06-01 11:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0003_auto_20200601_1044'),
        ('Configuration', '0005_organization_organizationhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organization',
            name='history',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='pastor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DB.ChurchMember'),
        ),
        migrations.DeleteModel(
            name='OrganizationHistory',
        ),
    ]
