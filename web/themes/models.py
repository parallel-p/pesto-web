from django.db import models
from stats.models import User, Theme, Participation

# Create your models here.
class UserResult(models.Model):
    theme = models.ForeignKey('stats.Theme')
    participation = models.ForeignKey('stats.Participation', null=True)
    solved = models.IntegerField()
    total = models.IntegerField(null=True)
