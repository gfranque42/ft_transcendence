# Generated by Django 5.0.7 on 2024-07-30 17:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_room_stats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='stats',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.game'),
        ),
    ]
