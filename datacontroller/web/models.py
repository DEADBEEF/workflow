from django.db import models
from django.contrib.auth.models import User


class Site(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    def __unicode__(self):
        return unicode(self.name)

# Create your models here.
JOB_TYPE = ((u'1', u'CLEAN'), (u'2', u'REGISTER'))
TYPE_LOOKUP = {}
for v,k in JOB_TYPE: TYPE_LOOKUP[k] = v
JOB_STATUS = ((u'1', u'NOTDONE'),(u'2', u'INPROGRESS'), (u'3', u'DONE'))
class Job(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    site = models.ForeignKey(Site)
    assignee = models.ForeignKey(User)
    job_type = models.CharField(max_length=1, choices=JOB_TYPE)
    job_status = models.CharField(max_length=1, choices=JOB_STATUS)
    description = models.TextField()




