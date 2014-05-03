
import datetime

from djorm_pgarray.fields import ArrayField

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc

now = datetime.datetime.utcnow().replace(tzinfo=utc)

HASH_LENGTH = 32

class File(models.Model):
    uuid = models.CharField(max_length=HASH_LENGTH)
    name = models.CharField(max_length=HASH_LENGTH)
    size = models.IntegerField()
    owner = models.ForeignKey(User)
    chunks = ArrayField(dbtype="int")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ((
            'uuid',
            'name',
            'size',
            'owner',
        ),)

class Chunk(models.Model):
    uuid = models.CharField(max_length=HASH_LENGTH)
    chunk_hash = models.CharField(max_length=HASH_LENGTH)
    validated = models.BooleanField()
    reference_count = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ((
            'uuid',
            'chunk_hash',
            'modified',
            'created',
        ),)

class Transfer(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user = models.ForeignKey(User, related_name='to_user')
    file_id = models.ForeignKey(File)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ((
            'from_user',
            'to_user',
            'file_id',
            'created',
            'modified',
        ),)

class ApiKey(models.Model):
    key = models.CharField(max_length=50)
    secret = models.CharField(max_length=50)
    enabled = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ((
            'key',
            'secret',
            'created',
            'modified',
        ),)

class WaitList(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ((
            'email',
            'created',
            'modified',
        ),)

