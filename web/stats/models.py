from django.db import models

class Season(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    order = models.IntegerField()
    class Meta:
        ordering = ['order']

class Parallel(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        ordering = ['name']

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    class Meta:
        ordering = ['last_name', 'first_name']

class Participation(models.Model):
    user = models.ForeignKey('User')
    season = models.ForeignKey('Season')
    parallel = models.ForeignKey('Parallel')

class Contest(models.Model):
    name = models.CharField(max_length=50)
    season = models.ForeignKey('Season')
    parallel = models.ForeignKey('Parallel')
    day = models.IntegerField()
    class Meta:
        ordering = ['day']
    
class Problem(models.Model):
    name = models.CharField(max_length=30)
    contest = models.ForeignKey('Contest')

class Language(models.Model):
    name = models.CharField(max_length=30)

class Submit(models.Model):
    problem = models.ForeignKey('Problem')
    participation = models.ForeignKey('Participation')
    outcome = models.CharField(max_length=2, choices=(
        ('OK', 'OK'),
        ('CE', 'Compilation Error'),
        ('RT', 'Runtime Error'),
        ('TL', 'Time-Limit Exceeded'),
        ('PE', 'Presentation Error'),
        ('WA', 'Wrong Answer'),
        ('CF', 'Check Failed'),
        ('PT', 'Partial Solution'),
        ('AC', 'Accepted for Testing'),
        ('IG', 'Ignored'),
        ('DQ', 'Disqualified'),
        ('PD', 'Pending'),
        ('ML', 'Memory Limit Exceeded'),
        ('SE', 'Secutity Violation'),
        ('SV', 'Style Violation'),
        ('WT', 'Wall Time Limit Exceeded'),
        ('PR', 'Pending Review'),
        ('RJ', 'Rejected'),
        ('SK', 'Skipped')))
    lang = models.ForeignKey('Language')

