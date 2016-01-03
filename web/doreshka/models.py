from django.db import models

# Create your models here.
class DinnerTime(models.Model):
    season = models.ForeignKey('stats.Season')
    dinner_delta = models.IntegerField()  # default is 14:00, 3600 means 15:00, -3600 - 13:00 and so on

class UserResult(models.Model):
    rj = models.IntegerField(null=True)
    pf = models.IntegerField(null=True)
    user = models.ForeignKey('stats.User')
    average_time = models.IntegerField()
    class Meta:
        ordering = ['-average_time']
