# Generated by Django 5.1.1 on 2024-09-09 18:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_series_series_duration_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seriesseasons',
            name='series_id',
        ),
        migrations.AddField(
            model_name='seriesseasons',
            name='series',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.series'),
        ),
    ]
