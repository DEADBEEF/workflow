from django.db import models
from django.contrib.auth.models import User


class Site(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    root = models.CharField(max_length=245)
    def __unicode__(self):
        return unicode(self.name)

# Create your models here.
JOB_TYPE = ((u'1', u'SERVER-1-1'), (u'2', u'SERVER-M-1'), (u'3', u'USER'))
TYPE_LOOKUP = {}
for v,k in JOB_TYPE: TYPE_LOOKUP[k] = v
JOB_STATUS = ((u'1', u'NOTDONE'),(u'2', u'INPROGRESS'), (u'3', u'TRANSFER_BACK') , (u'4', u'DONE'))
STATUS_LOOKUP = {}
for v,k in JOB_STATUS: STATUS_LOOKUP[k] = v
class Job(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    type = models.CharField(max_length=1, choices=JOB_TYPE)
    script = models.CharField(max_length=200,blank=True)
    description = models.TextField(blank=True)

class File(models.Model):
    filename = models.CharField(max_length=500)

class Task(models.Model):
    site = models.ForeignKey(Site)
    job_type = models.ForeignKey(Job)
    assignee = models.ForeignKey(User)
    input_files = models.ManyToManyField(File, blank=True)
    output_folder = models.CharField(max_length=255)
    predecessors = models.ManyToManyField("self", blank=True)
    successors = models.ManyToManyField("self", blank=True)
    job_status = models.CharField(max_length=1, choices=JOB_STATUS)


