from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE


# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    conclusion_date = models.DateTimeField(null=True, blank=True)

    important = models.BooleanField(default=False)

    owner = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.title
