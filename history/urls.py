from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from history import views


urlpatterns = patterns('history.views',
    # url(r'^$', 'history', name='history'),
    # url(r'^historytable$', login_required(views.history_table.as_view()), name='historytable'),
    url(r'^$', never_cache(login_required(views.history.as_view())), name='history'),
    # url(r'table$', login_required(views.history_table.as_view()), name='table'),
    url(r'^(?P<id>\w+)/results/$', 'results', name='results'),
    url(r'^(?P<history_id>\w+)/comments/$', 'result_comments', name='result-comments'),
    url(r'^(?P<history_id>\w+)/follow/$', 'followResult', name='follow'),
    url(r'^(?P<history_id>\w+)/unfollow/$', 'unfollowResult', name='unfollow'),
    url(r'^(?P<uid>\w+)/show/$', never_cache(login_required(views.history.as_view())), name='history'),
    url(r'^(?P<id>\w+)/jobinfo/$', 'jobinfo', name='jobinfo'),
    url(r'^(?P<id>\w+)/tail-file/$', 'tailFile', name='tailFile'),
    url(r'^change-flag/$', 'changeFlag', name='changeFlag'),
    url(r'^cancel-slurmjob/$', 'cancelSlurmjob', name='cancelSlurmjob'),
    url(r'^(?P<id>\w+)/(?P<type>\w+)/generate-caption/$', 'generate_caption', name='generate-caption'),
    url(r'^(?P<history_id>\w+)/(?P<deleted>\w+)/count-notes/$', 'count_notes', name='count-notes'),
    url(r'^(?P<history_id>\w+)/(?P<tag_id>\w+)/edit-historytag/$', 'edit_htag', name='edit-historytag'),
    url(r'^sendmail/$', 'sendMail', name='sendMail'),
)
