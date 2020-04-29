from django.db import models
from django.conf import settings
from user_profile.models import User


# represent database structure as classes
# classes are called models
# django already has user model created that we will use

# py manage.py makemigrations
# look @ /migrations/0001_initial.py

# to view SQL code of above
# py manage.py sqlmigrate blog 0001
# takes class we created and writes out SQL for all fields to be compatible w/ DB we use

# py manage.py migrate
# allows us to make changes to DB even after we have data in there w/o use of SQL


class Post(models.Model):
    # each attribute will be different field in DB
    # primary key identifier for Post object
    id = models.AutoField(primary_key=True)
    # max_length restraint
    title = models.CharField(max_length=100, null=True, blank=True)
    # TextField similar to CharField but w/o restrictions
    content = models.TextField()
    # media field for media uploads. Store media path as char field.
    media = models.CharField(max_length =100, null=True, blank=True)
    # auto_now_add set date_posed to current date and time
    # can't ever update - won't allow for edits
    date_posted = models.DateTimeField(auto_now_add=True)
    # pulls User from separate table created by django
    # one-to-many relationship // one user can have multiple posts, but a post can only have 1 author
    # ForeignKey(related table, what to do if user who created post gets deleted - delete post)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.IntegerField(default=0)
    parent_id = models.IntegerField(null=True, blank=True)

    # return how we want Post to be printed out
    def __str__(self):
        return str(self.title) if self.title else ''


""""
class Friend(models.Model):
    users = models.ManyToManyField(User)    #everyone else

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)
"""