# Generated by Django 5.0.7 on 2024-07-30 16:28

import app.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_room_stats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='stats',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.Game'),
        ),
    ]