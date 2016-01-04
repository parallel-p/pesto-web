"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
import stats.views

urlpatterns = [
    url(r'^', include('stats.urls')),
    url(r'^', include('themes.urls')),
    url(r'^doreshka/', include('doreshka.urls')),
    url(r'^admin/themes', stats.views.admin_themes, name='admin_themes'),
    url(r'^admin/', admin.site.urls),
]
handler400 = 'stats.views.bad_request'
handler403 = 'stats.views.permission_denied'
handler404 = 'stats.views.page_not_found'
handler500 = 'stats.views.server_error'