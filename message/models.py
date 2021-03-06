from django.db import models
from user_profile.models import User
from django.conf import settings


class Message(models.Model):
    # primary key identifier for Message object
    id = models.AutoField(primary_key=True)
    # TextField similar to CharField but w/o restrictions
    content = models.TextField()
    # can't ever update - won't allow for edits
    date_posted = models.DateTimeField(auto_now_add=True)
    # ForeignKey(related table, what to do if user who created post gets deleted - delete post)
    author = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, null=True, blank=True)
    recipient = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE, null=True, blank=True)
    seen = models.BooleanField(default=False)

    # return how we want to be printed out
    def __str__(self):
        return self.content
