from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=200)
    assignee = models.ForeignKey(User)
    job_type = models.CharField(max_length=1, choices=(('1', 'CLEAN'),
                                                       ('2', 'REGISTER')))
    job_status = models.CharField(max_length=1, choices=(('1', 'NOTDONE'),
                                                         ('2', 'INPROGRESS'),
                                                         ('3', 'DONE')))
    description = models.TextField()


