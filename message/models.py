from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Message(models.Model):
    # primary key identifier for Post object
    id = models.AutoField(primary_key=True)
    # TextField similar to CharField but w/o restrictions
    content = models.TextField()
    # can't ever update - won't allow for edits
    date_posted = models.DateTimeField(auto_now_add=True)
    # ForeignKey(related table, what to do if user who created post gets deleted - delete post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    # recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    # return how we want to be printed out
    def __str__(self):
        return self.content
