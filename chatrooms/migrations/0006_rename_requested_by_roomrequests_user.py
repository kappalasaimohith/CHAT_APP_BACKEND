# Generated by Django 5.0.7 on 2024-07-26 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatrooms', '0005_roomrequests'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomrequests',
            old_name='requested_by',
            new_name='user',
        ),
    ]