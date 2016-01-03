from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /compare/1,2
    url(r'^compare/(?P<users>[0-9]+(,[0-9]+)*)/$', views.compare, name='compare'),
]
