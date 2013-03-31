
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc

now = datetime.datetime.utcnow().replace(tzinfo=utc)

HASH_LENGTH = 32

class WaitList(models.Model):
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

