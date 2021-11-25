import requests
from django.db import models

from accounts.models import CustomUser


class Projects(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='author_user_id')

    def __str__(self):
        return self.title