# Generated by Django 2.2.6 on 2019-11-17 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickshort', '0005_auto_20191116_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortenedurl',
            name='stats_key',
            field=models.TextField(max_length=10, null=True, unique=True),
        ),
    ]
