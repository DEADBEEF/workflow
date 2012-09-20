from  django.contrib import admin
from web.models import  Job ,  Site, Task,File, Host, SiteDir, Category

class JobAdmin(admin.ModelAdmin):
   list_display = ["name", 'type']

admin.site.register(Job,JobAdmin)
admin.site.register(Site)
admin.site.register(SiteDir)
admin.site.register(Task)
admin.site.register(File)
admin.site.register(Host)
admin.site.register(Category)
