# Generated by Django 5.1.1 on 2024-09-10 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_continuewatchingfilm_continuewatchingseries'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLikeList',
            fields=[
                ('like_id', models.AutoField(primary_key=True, serialize=False)),
                ('film', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.film')),
                ('series', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.series')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.usersapp')),
            ],
        ),
    ]