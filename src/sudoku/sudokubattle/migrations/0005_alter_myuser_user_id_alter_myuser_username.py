# Generated by Django 4.2 on 2024-10-06 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sudokubattle', '0004_sudokuroom_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='user_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]