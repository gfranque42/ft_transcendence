# Generated by Django 4.2 on 2024-09-23 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapi', '0014_userprofile_jwt'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_winner', models.IntegerField(blank=True, null=True)),
                ('score_loser', models.IntegerField(blank=True, null=True)),
                ('game_type', models.CharField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('loser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_loss', to='authapi.userprofile')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_won', to='authapi.userprofile')),
            ],
        ),
    ]