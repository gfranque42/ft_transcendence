# Generated by Django 5.0.7 on 2024-07-31 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_room_stats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='stats',
        ),
        migrations.DeleteModel(
            name='Game',
        ),
    ]
