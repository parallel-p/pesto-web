from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /rating
    url(r'^rating$', views.doreshka_rating, name='doreshka_rating'),
]
