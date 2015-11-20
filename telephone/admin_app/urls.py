from django.conf.urls import url
from telephone.admin_app.views import create_new_user, get_archive_transacts, get_pending_transacts, \
	get_history_transacts, test_routes

urlpatterns = [
	url(r'^newuser/$', create_new_user, {'template': 'create_new_user.html'}),
	url(r'^getPendingTransacts/$', get_pending_transacts, {'template': 'pending_transacts.html'}),
	url(r'^getArchiveTransacts/$', get_archive_transacts, {'template': 'archive_transacts.html'}),
	url(r'^getHistoryTransacts/$', get_history_transacts, {'template': 'history_transacts.html'}),
	url(r'^tr/', test_routes)
]