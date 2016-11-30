"""file_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from admin_app import views
from file_server import settings
from user_app import views as user_views

from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^admin/users/add', views.add_user),
    url(r'^admin/groups/add', views.add_group),
    url(r'^search', views.search_user),
    url(r'^admin/users/(?P<user_id>\d+)', views.user_groups),

    url(r'^user/(?P<user_id>\d+)/catalogues', user_views.list_catalogues),
    url(r'^user/catalogues/add', user_views.add_catalogue),
    url(r'^catalogue/(?P<cat_id>\d+)$', user_views.catalogue),
    url(r'^catalogue/(?P<cat_id>\d+)/file/upload', user_views.upload_file)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_DIR)
