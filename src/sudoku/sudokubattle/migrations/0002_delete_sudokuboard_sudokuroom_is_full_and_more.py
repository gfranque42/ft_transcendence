# Generated by Django 4.2 on 2024-09-26 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sudokubattle', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SudokuBoard',
        ),
        migrations.AddField(
            model_name='sudokuroom',
            name='is_full',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sudokuroom',
            name='player1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sudokuroom',
            name='player2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sudokuroom',
            name='difficulty',
            field=models.IntegerField(choices=[(0, 'Easy'), (1, 'Medium'), (2, 'Hard')]),
        ),
        migrations.AlterField(
            model_name='sudokuroom',
            name='url',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
