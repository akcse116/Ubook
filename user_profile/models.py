from django.db import models
from django.contrib.auth.models import AbstractUser


def default_prof_pic():
    return 'media/cookie.jpeg'


class User(AbstractUser):
    prof_pic = models.ImageField(null=True, default=default_prof_pic())
    # ----
    #friends = models.BinaryField(null=True)
    # ----
    
    def __str__(self):
        return self.username
