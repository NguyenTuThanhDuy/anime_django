# Generated by Django 5.1.1 on 2024-11-20 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_channel_channel_id_alter_video_video_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='channel_hash',
            field=models.CharField(db_index=True, null=True, unique=True),
        ),
    ]
