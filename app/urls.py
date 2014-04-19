from django.conf.urls import patterns, include, url

urlpatterns = patterns('app.views',
    url(r'^$', 'home'),
    url(r'^(?P<page>\d+)$', 'home'),
    url(r'^archives$', 'archives'),
    url(r'^post/(?P<slug>[^/]+)$', 'single'),
)
