from django.conf.urls import url, patterns

urlpatterns = patterns('history.views',
    url(r'^$', 'history', name='history'),
    url(r'^(?P<id>\w+)/results/$', 'results', name='results'),
    url(r'^(?P<id>\w+)/tail-file/$', 'tailFile', name='tailFile'),
)