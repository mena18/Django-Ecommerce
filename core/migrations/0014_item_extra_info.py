# Generated by Django 2.2 on 2020-07-22 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20200208_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='extra_info',
            field=models.TextField(null=True, verbose_name=True),
        ),
    ]