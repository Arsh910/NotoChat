# Generated by Django 5.0.6 on 2024-06-26 08:21

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videochat', '0003_video_room_v_author_alter_video_room_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video_room',
            name='name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=128, unique=True),
        ),
    ]
