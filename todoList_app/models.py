from django.db import models
from string import Template
from django.contrib.auth.models import User
# Create your models here.
class TaskList(models.Model):
    manage = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    task = models.CharField(max_length=30)
    done = models.BooleanField(default=False)

    def __str__(self):
        t = Template('$task completed $done')
        s = t.substitute(task=self.task, done=self.done)
        return s