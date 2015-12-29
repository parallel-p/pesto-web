from django.db import models
from stats.models import User, Theme

# Create your models here.
class UserResult(models.Model):
    user = models.ForeignKey('stats.User')
    theme = models.ForeignKey('stats.Theme')
    year = models.IntegerField()
    solved = models.IntegerField()