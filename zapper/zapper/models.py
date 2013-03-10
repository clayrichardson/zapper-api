from django.db import models
from django.contrib.auth.models import User

class UserToFile(models.Model):
    user = models.ForeignKey(User)
    file_id = models.ForeignKey(File)
    class Meta:
        unique_together = (('user', 'file_id'),)
