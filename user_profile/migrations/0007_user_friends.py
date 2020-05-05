# Generated by Django 3.0.3 on 2020-05-05 21:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_remove_user_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, default=None, related_name='_user_friends_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
