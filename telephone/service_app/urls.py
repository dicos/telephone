from django.conf.urls import url
from telephone.service_app.controllers import get_api_urls, get_oauth_token, generate_password, create_mail, \
	get_mailbox_data, transact_action, get_transact_id
from telephone.service_app.error_pages import default_error

urlpatterns = [
	url(r'^getApiUrls/', get_api_urls),
	url(r'^getOAuthToken/', get_oauth_token),
	url(r'^generatePassword/$', generate_password),
	url(r'^createMail/$', create_mail),
	url(r'^getMailboxData/$', get_mailbox_data),
	url(r'^transactAction/(?P<action>confirm|cancel|archive|create_user)/$', transact_action),
	url(r'^getTransactId/$', get_transact_id),

	url(r'e/$', default_error, {'template': 'default_error.html'})
]
