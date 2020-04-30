# Generated by Django 3.0.4 on 2020-04-28 21:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_friend_current_user'),
        ('user_profile', '0003_auto_20200428_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_user_friends_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='likedPosts',
            field=models.ManyToManyField(blank=True, default=None, to='blog.Post'),
        ),
    ]