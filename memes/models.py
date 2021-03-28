from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Modal for CreateMeme
class CreateMeme(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100)
    url = models.URLField()
    caption = models.CharField(max_length=100)
        
    def __str__(self):
        return str(self.id)
