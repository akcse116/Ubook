from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=500, null=True, blank=True)
    friends = models.ManyToManyField('self', default=None, blank=True)

    def __str__(self):
        return str(self.username) if self.username else ''
