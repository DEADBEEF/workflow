from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'datacontroller.views.home', name='home'),
    # url(r'^datacontroller/', include('datacontroller.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^', include('web.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
)
