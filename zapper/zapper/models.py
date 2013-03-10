
from django.db import models
from django.contrib.auth.models import User

HASH_LENGTH = 32

class File(models.Model):
    uuid = models.CharField(max_length=HASH_LENGTH)
    name = models.CharField()
    size = models.IntegerField()
    owner = models.ForeignKey(User)
    chunks = models.ForeignKey(FileChunk)

class Chunk(models.Model):
    uuid = models.CharField(max_length=HASH_LENGTH)
    chunk_hash = models.CharField(max_length=HASH_LENGTH)
    validated = modles.BooleanField()
    reference_count = models.IntegerField()

class Transfer(models.Model):
    from_user = models.ForeignKey(User)
    to_user = models.ForeignKey(User)
    file_id = models.ForeignKey(File)

class UserToFile(models.Model):
    user = models.ForeignKey(User)
    file_id = models.ForeignKey(File)
    class Meta:
        unique_together = (('user', 'file_id'),)
