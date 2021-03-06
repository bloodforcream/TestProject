# Generated by Django 3.0.3 on 2020-02-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200229_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='account',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Счет в рублях'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='inn',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='ИНН'),
        ),
    ]
