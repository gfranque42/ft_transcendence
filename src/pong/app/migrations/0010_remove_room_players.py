# Generated by Django 5.1.1 on 2024-10-07 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_player_stanid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='players',
        ),
    ]
