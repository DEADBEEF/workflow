from django.db import models
from django.contrib.auth.models import User



# Create your models here.
JOB_TYPE = ((u'1', u'SERVER-1-1'), (u'2', u'SERVER-M-1'), (u'3', u'USER'))
TYPE_LOOKUP = {}
for v,k in JOB_TYPE: TYPE_LOOKUP[k] = v
JOB_STATUS = ((u'1', u'NOTDONE'),(u'2', u'INPROGRESS'), (u'3', u'TRANSFER_BACK') , (u'4', u'DONE'))
STATUS_LOOKUP = {}
for v,k in JOB_STATUS: STATUS_LOOKUP[k] = v

class Site(models.Model):
    name = models.CharField(max_length=30,primary_key=True)
    folder_name = models.CharField(max_length=30,default="")
    def __unicode__(self):
        return unicode(self.name)

class Job(models.Model):
    name = models.CharField(max_length=200,primary_key=True)
    type = models.CharField(max_length=1, choices=JOB_TYPE)
    script = models.CharField(max_length=200,blank=True)
    description = models.TextField(blank=True)
    def __unicode__(self):
        return unicode(self.name)

class Host(models.Model):
    user = models.ForeignKey(User)
    hostname = models.CharField(max_length=100)
    root_dir = models.CharField(max_length=300)
    primary = models.BooleanField(default=True)
    def __unicode__(self):
        return u"{0} : {1}".format(self.user, self.hostname)

class File(models.Model):
    filename = models.CharField(max_length=500)
    site = models.ForeignKey(Site)
    def __unicode__(self):
        return unicode(self.filename)

class SiteDir(models.Model):
    root_dir = models.CharField(max_length=100)
    def __unicode__(self):
        return unicode(self.root_dir)



class Task(models.Model):
    site = models.ForeignKey(Site)
    job_type = models.ForeignKey(Job)
    assignee = models.ForeignKey(User)
    input_files = models.ManyToManyField(File, blank=True)
    output_folder = models.CharField(max_length=255)
    predecessors = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="pred+")
    successors = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="succ+")
    job_status = models.CharField(max_length=1, choices=JOB_STATUS)
    def __unicode__(self):
        return u"{0}:{1} - {2}".format(self.site, self.job_type, self.assignee)



