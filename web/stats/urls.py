from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /users
    url(r'^users$', views.users, name='users'),
    # ex: /user/1
    url(r'^user/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    # ex: /similar_users/1
    url(r'^similar_users/(?P<user_id>[0-9]+)/$', views.similar_users, name='similar_users'),
    # ex: /home
    url(r'^home$', views.home, name='home'),
]
