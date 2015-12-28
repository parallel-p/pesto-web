from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    @classmethod
    def create(self, first_name, last_name):
      return self(first_name=first_name, last_name=last_name)


class Submit(models.Model):
    problem_id = models.CharField(max_length=30)
    submit_id = models.CharField(max_length=30)
    outcome = models.CharField(max_length=30)
    user_id = models.CharField(max_length=30)
    lang_id = models.CharField(max_length=30)
    scoring = models.CharField(max_length=30)

    @classmethod
    def create(self, problem_id, submit_id, outcome, user_id, lang_id, scoring):
      return self(problem_id=problem_id, submit_id=submit_id, outcome=outcome, user_id=user_id, lang_id=lang_id, scoring=scoring)


class Problem:
    problem_id = models.CharField(max_length=30)
    polygon_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    @classmethod
    def create(self, problem_id, polygon_id, name):
      return self(problem_id=problem_id, polygon_id=polygon_id)


class Contest:
    contest_id = models.CharField(max_length=30)
    origin = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    scoring = models.CharField(max_length=30)

    @classmethod
    def create(self, contest_id, origin, name, scoring):
      return self(contest_id=contest_id, origin=origin, name=name, scoring=scoring)


