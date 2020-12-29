from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Entry(models.Model):
    data = models.CharField(unique=False, max_length=10)
    def __str__(self):
        return str(self.id)
    

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)