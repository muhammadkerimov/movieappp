# Generated by Django 5.1.1 on 2024-09-09 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_seriesepisodes_series_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seriesepisodes',
            old_name='series_id',
            new_name='series',
        ),
    ]