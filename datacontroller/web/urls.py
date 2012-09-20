from django.conf.urls import patterns, url, include


urlpatterns = patterns('web.views',
        url(r'^$','index'),
        url(r'^task/(?P<site>\w+)/(?P<task_id>\w+)/$', 'task', name='task-summary'),
        url(r'^edit/(?P<site>\w+)/(?P<task_id>\w+)/$', 'edit_task', name='task-edit'),
        url(r'^finish/$', 'finish_task'),
        url(r'^transfer/$', 'start_transfer'),
        url(r'^upload/$', 'upload'),
        url(r'^site/(?P<site>\w+)/$', 'view_site'),
        url(r'^site/', 'sites'),
        url(r'^addtask/$', 'add_task'),
        url(r'^runtask/$', 'run_task'),
        url(r'^addjob/$', 'add_job'),
        url(r'^updatejob/$', 'update_job'),
        url(r'^getjob/$', 'get_job'),
        url(r'^addcategory/$', 'add_category'),
        url(r'^addsite/$', 'add_site'),
        )
