# Generated by Django 3.0.3 on 2020-05-05 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0005_user_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='friends',
        ),
    ]
