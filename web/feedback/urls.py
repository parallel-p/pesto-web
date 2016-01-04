from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /form
    url(r'^form$', views.feedback, name='feedback_form'),
    # ex: /admin
    url(r'^admin$', views.admin, name='feedback_admin'),
]
