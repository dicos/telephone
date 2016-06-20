# coding=utf-8
import datetime
from django import template
from telephone import settings
from telephone.my_app.services.PBXService import PBXService
from telephone.service_app.services.PBXDataService import PBXDataService

register = template.Library()


@register.inclusion_tag('profile_info_phone.html', takes_context=True)
def profile_info_phone(context, cls, url, state=None):
	def ending_resolver(value):
		endings = ['дня', 'дней']
		return 'день' if value == 1 else (endings[0] if 2 <= value <= 4 else endings[1])

	user = context['user']
	icon_cls = 'icon'
	text_type = ''

	subscription = user.get_current_subscription()
	end_date = subscription.get_end_date()

	days_remains = subscription.days_remain()

	if not days_remains:
		title = 'Подписка не оформлена'
		icon_cls += '-warning'
		text_type += ' text-warning'
	elif days_remains > 7:
		title = 'Оплачено до {date}'.format(date=end_date.strftime(settings.DATE_CLIENT_FORMAT))
		icon_cls += '-checkmark text-success'
		text_type = 'text-success'
	elif days_remains == 0:
		title = 'Подписка истекает сегодня'
		icon_cls += '-warning'
		text_type += ' text-warning'
	elif days_remains < 0:
		days = abs(days_remains)
		title = 'Обслуживание номера остановлено. Через {days} {ending} он будет утрачен безвозвратно'\
			.format(days=days, ending=ending_resolver(days))
		icon_cls += '-cancel-circle'
		text_type += ' text-danger'
	else:
		days = abs(days_remains)
		title = 'До отключения номера осталось {days} {ending}. Нажмите чтобы оплатить'\
			.format(days=days, ending=ending_resolver(days))
		icon_cls += '-notification'
		text_type += ' text-warning'

	return {
		'phone': {
			'cls': cls,
			'text_type': text_type,
			'title': title,
			'url': url,
			'icon': icon_cls,
			'value': user.pbx.phone_number,
			'state': state
		}
	}


@register.inclusion_tag('profile_info_cash.html', takes_context=True)
def profile_info_cash(context, cls, url, state=None):
	user = context['user']

	service = PBXService(user.pbx)
	balance = service.get_balance()

	return {
		'cash': {
			'cls': cls,
			'text_type': '',
			'title': '',
			'url': url,
			'icon': 'icon-credit-card',
			'value':  '%.2f руб.' % balance if balance else 'Баланс временно недоступен',
			'state': state
		}
	}
