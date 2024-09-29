# Generated by Django 4.2 on 2024-08-30 16:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SudokuBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row1', models.CharField(default='---------', max_length=9)),
                ('row2', models.CharField(default='---------', max_length=9)),
                ('row3', models.CharField(default='---------', max_length=9)),
                ('row4', models.CharField(default='---------', max_length=9)),
                ('row5', models.CharField(default='---------', max_length=9)),
                ('row6', models.CharField(default='---------', max_length=9)),
                ('row7', models.CharField(default='---------', max_length=9)),
                ('row8', models.CharField(default='---------', max_length=9)),
                ('row9', models.CharField(default='---------', max_length=9)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SudokuRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100, unique=True)),
                ('difficulty', models.IntegerField()),
                ('board', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
