# Generated by Django 5.0.7 on 2024-07-25 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatrooms', '0003_roommember_member'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='room_name',
            new_name='room',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='room_name',
            new_name='room',
        ),
    ]
