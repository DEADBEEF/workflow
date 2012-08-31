from  django.contrib import admin
from web.models import Job, Site, Task,File

class JobAdmin(admin.ModelAdmin):
   list_display = ["name", 'type']

admin.site.register(Job,JobAdmin)
admin.site.register(Site)
admin.site.register(Task)
admin.site.register(File)
