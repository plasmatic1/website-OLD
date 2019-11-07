from django.db import models
from datetime import datetime, timedelta

# Create your models here.
from django.db.models import Model


class Subject(Model):
    name = models.CharField(max_length=256, verbose_name='Name')

    def __str__(self):
        return self.name


ONE_DAY = timedelta(days=1)


class Homework(Model):
    name = models.CharField(max_length=256, verbose_name='Name')
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, verbose_name='Subject')
    due_date = models.DateField(verbose_name='Due Date')
    comments = models.CharField(max_length=1024, verbose_name='Comments')

    @property
    def has_comments(self):
        return len(self.comments) > 0

    @property
    def overdue(self):
        return self.due_date <= datetime.now().date()

    @property
    def due_tommorow(self):
        return self.due_date - ONE_DAY <= datetime.now().date()


VALID_PROBLEM_TYPES = ['dmoj', 'cf', 'atcoder', 'kattis']


class Problem(Model):
    name = models.CharField(max_length=64, verbose_name='Name')
    link = models.CharField(max_length=128, verbose_name='Link')
    type = models.CharField(max_length=64, verbose_name='Type')
    difficulty = models.IntegerField(verbose_name='Difficulty', default=-1)

    @property
    def has_name(self):
        return len(self.name) > 0


class Project(Model):
    name = models.CharField(max_length=256, verbose_name='Name')
    description = models.CharField(max_length=256, verbose_name='Description', default='')
