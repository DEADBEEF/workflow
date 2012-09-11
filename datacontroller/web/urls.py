from django.conf.urls import patterns, url, include


urlpatterns = patterns('web.views',
        url(r'^$','index'),
        url(r'^task/(?P<site>\w+)/(?P<task_id>\w+)/', 'task', name='task-summary'),
        url(r'^finish/$', 'finish_task'),
        url(r'^transfer/$', 'start_transfer'),
        url(r'^upload/$', 'upload'),
        )