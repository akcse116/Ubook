from django.db import models
from django.contrib.auth.models import User


# represent database structure as classes
# classes are called models
# django already has user model created that we will use


class Post(models.Model):
    # each attribute will be different field in DB

    # max_length restraint
    title = models.CharField(max_length=100)
    # TextField similar to CharField but w/o restrictions
    content = models.TextField()
    # auto_now_add set date_posed to current date and time
    # can't ever update - won't allow for edits
    date_posted = models.DateTimeField(auto_now_add=True)
    # pulls User from separate table created by django
    # one-to-many relationship // one user can have multiple posts, but a post can only have 1 author
    # ForeignKey(related table, what to do if user who created post gets deleted - delete post)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
