# Generated by Django 4.2.1 on 2023-06-03 18:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_tweet', '0003_meeps'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Meeps',
            new_name='Meep',
        ),
    ]
