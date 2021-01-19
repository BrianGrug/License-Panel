from django.conf.urls import url

from polls.views import DetailView, IndexView, ResultView, vote

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/detail/$', DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/result/$', ResultView.as_view(), name='result'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', vote, name='vote'),
]
