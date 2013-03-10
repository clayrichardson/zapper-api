from django.db import models
from django.contrib.auth.models import User

HASH_LENGTH = 32

class File(models.Model):
    uuid = models.CharField(max_length=HASH_LENGTH)
    name = models.CharField()
    size = models.IntegerField()
    owner = models.ForeignKey(User)

class Chunk(models.Model):
    uuid = models.CharField(max_length=HASH_LENGTH)
    chunk_hash = models.CharField(max_length=HASH_LENGTH)
    validated = modles.BooleanField()
    reference_count = models.IntegerField()

class FileToChunk(models.Model):
    file_id = models.ForeignKey(File)
    chunk = models.ForeignKey(FileChunk)
    position = models.IntegerField()
    class Meta:
        unique_together = (('file_id', 'chunk', 'position'),)

class Transfer(models.Model):
    from_user = models.ForeignKey(User)
    to_user = models.ForeignKey(User)
    file_id = models.ForeignKey(File)

class UserToFile(models.Model):
    user = models.ForeignKey(User)
    file_id = models.ForeignKey(File)
    class Meta:
        unique_together = (('user', 'file_id'),)
