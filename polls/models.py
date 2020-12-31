from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Entry(models.Model):
    data = models.CharField(unique=False, max_length=10)
    def __str__(self):
        return str(self.id)

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.CharField(max_length=100)
    def __str__(self):
        return str(self.data)

class ChatMessage(models.Model):
    user_to = models.ForeignKey(User, on_delete=models.CASCADE)
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_stuf')
    message = models.CharField(max_length = 100)
    
    def __str__(self):
        return str(self.user_from) + ": " + str(self.message)