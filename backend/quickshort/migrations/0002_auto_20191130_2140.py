# Generated by Django 2.2.6 on 2019-11-30 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickshort', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortenedurl',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]