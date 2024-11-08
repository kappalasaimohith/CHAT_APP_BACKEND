# Generated by Django 5.0.7 on 2024-07-12 07:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=30, unique=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_auth.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sent_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_auth.customuser')),
                ('room_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chatrooms.room')),
            ],
        ),
    ]
