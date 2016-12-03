from django.conf.urls import url
from admin_app import views
from file_server import settings
from user_app import views as user_views

from django.conf.urls.static import static

# TODO - url names, тег {% url %}

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
    url(r'^file/(?P<file_id>\d+)$', user_views.file_detail, name='file'),
    url(r'^catalogue/(?P<cat_id>\d+)$', user_views.catalogue_detail),
    url(r'^catalogue/(?P<cat_id>\d+)/file/upload', user_views.upload_file)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_DIR)
