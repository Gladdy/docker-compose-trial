# Generated by Django 2.2.6 on 2019-11-16 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickshort', '0004_shortenedurl_stats_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortenedurl',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
