from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=2016)
    time = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-time']
