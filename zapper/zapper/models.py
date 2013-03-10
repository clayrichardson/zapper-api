from django.db import models
from django.contrib.auth.models import User

HASH_LENGTH = 32

class File(models.Model):
    uuid = models.CharField(max_length=HASH_LENGTH)
    name = models.CharField(max_length=HASH_LENGTH)
    size = models.IntegerField()
    owner = models.ForeignKey(User)
    class Meta:
        unique_together = (('uuid', 'name', 'size', 'owner'),)

class Chunk(models.Model):
    uuid = models.CharField(max_length=HASH_LENGTH)
    chunk_hash = models.CharField(max_length=HASH_LENGTH)
    validated = models.BooleanField()
    reference_count = models.IntegerField()
    class Meta:
        unique_together = (('uuid', 'chunk_hash'),)

class FileToChunk(models.Model):
    file_id = models.ForeignKey(File)
    chunk = models.ForeignKey(Chunk)
    position = models.IntegerField()
    class Meta:
        unique_together = (('file_id', 'chunk', 'position'),)

class Transfer(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user = models.ForeignKey(User, related_name='to_user')
    file_id = models.ForeignKey(File)
    class Meta:
        unique_together = (('from_user', 'to_user', 'file_id'),)

class UserToFile(models.Model):
    user = models.ForeignKey(User)
    file_id = models.ForeignKey(File)
    class Meta:
        unique_together = (('user', 'file_id'),)

