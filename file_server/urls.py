from django.conf.urls import url
from admin_app import views
from file_server import settings
from user_app import views as user_views

from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),

    url(r'^admin/users/add', views.add_user, name='user-add'),
    url(r'^admin/groups/add$', views.add_group, name='group-add'),
    url(r'^admin/groups/add_catalogue', views.add_catalogue_to_group, name='add-catalogue-to-group'),
    url(r'^admin/groups/change_catalogue', views.change_catalogues_in_group, name='change-catalogues-in-group'),
    url(r'^admin/search', views.search, name='admin-search'),
    url(r'^admin/users/(?P<user_id>\d+)', views.user_groups_list),
    url(r'^admin/user_groups/add_user', views.add_user_to_group, name='add-user-to-group'),
    url(r'^admin/user_groups/delete_user', views.delete_user_from_group, name='delete-user-from-group'),
    url(r'^admin/groups/(?P<group_id>\d+)', views.group_catalogues),
    url(r'^admin/users/report', views.users_report, name='users-report'),

    url(r'^user/(?P<user_id>\d+)/catalogues', user_views.list_catalogues),
    url(r'^user/catalogues/add', user_views.add_catalogue, name='catalogue-add'),
    url(r'^file/(?P<file_id>\d+)$', user_views.file_detail, name='file'),
    url(r'^file/delete$', user_views.file_delete, name='file-delete'),
    url(r'^catalogue/(?P<cat_id>\d+)$', user_views.catalogue_detail),
    url(r'^catalogue/(?P<cat_id>\d+)/file/upload', user_views.upload_file),
    url(r'^catalogue/delete$', user_views.catalogue_delete, name='catalogue-delete')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_DIR)
