from  django.contrib import admin
from web.models import Job, Site

class JobAdmin(admin.ModelAdmin):
   list_display = ["name",'assignee', 'site', 'job_type', 'job_status']

admin.site.register(Job,JobAdmin)
admin.site.register(Site)
