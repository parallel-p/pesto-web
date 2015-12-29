from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /1
    url(r'^(?P<user_id>[0-9]+)/$', views.by_user, name='by_user'),
]
