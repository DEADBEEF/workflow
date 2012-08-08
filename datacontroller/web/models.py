from django.db import models
from django.contrib.auth.models import User


class Site(models.Model):
    name = CharField(max_lengh=30)
# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    site = models.ForgeinKey(Site)
    assignee = models.ForeignKey(User)
    job_type = models.CharField(max_length=1, choices=(('1', 'CLEAN'),
                                                       ('2', 'REGISTER')))
    job_status = models.CharField(max_length=1, choices=(('1', 'NOTDONE'),
                                                         ('2', 'INPROGRESS'),
                                                         ('3', 'DONE')))
    description = models.TextField()




