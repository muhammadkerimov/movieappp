# Generated by Django 5.1.1 on 2024-09-09 19:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_seriesepisodes_series_seasons_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriesepisodes',
            name='series_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.series'),
        ),
    ]