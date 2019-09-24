from django.db import models

# Create your models here.
from django.db.models import Model


class Subject(Model):
    name = models.CharField(max_length=256, verbose_name='Name')


class Homework(Model):
    name = models.CharField(max_length=256, verbose_name='Name')
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, verbose_name='Subject')
    due_date = models.DateField(verbose_name='Due Date')
    comments = models.CharField(max_length=1024, verbose_name='Comments')


class Problem(Model):
    name = models.CharField(max_length=256, verbose_name='Name')
    link = models.CharField(max_length=256, verbose_name='Link')
    difficulty = models.IntegerField(verbose_name='Difficulty')
