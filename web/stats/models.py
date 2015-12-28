from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    @classmethod
    def create(self, first_name, last_name):
      return self(first_name=first_name, last_name=last_name)

class Problem(models.Model):
    polygon_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    @classmethod
    def create(self, polygon_id, name):
      return self(polygon_id=polygon_id, name=name)

class Submit(models.Model):
    problem = models.ForeignKey('Problem')
    outcome = models.CharField(max_length=30)
    user = models.ForeignKey('User')
    lang_id = models.CharField(max_length=30)

class Contest:
    name = models.CharField(max_length=30)

    @classmethod
    def create(self, name):
      return self(name=name)
