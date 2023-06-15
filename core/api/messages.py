from django.utils.translation import gettext_lazy as _

# serializers
SPOT_DOES_NOT_EXIST = _("Окно с таким spot_id не существует")
SPOT_ALREADY_EXIST = _("Такое окно уже существует")
SPOT_ALREADY_BOOKED = _("Окно уже забронировано")
INCORRECT_SPOT_TIME = _("Неверная продолжительность сессии")
INCORRECT_SPOT_DURATION = _("Возможные интервалы сессии 60, 90, 120 минут")
INCORRECT_DATE_FORMAT = _("Некорректный формат даты")
INCORRECT_DATE = _("Дата окна не может быть в прошлом")
CUSTOMER_DOES_NOT_EXIST = _("Пользователя с таким customer_id не существует")

# views
NO_FIELDS_CUSTOMER_DATE = _("Не заданы поля customer_id, date")
NO_FIELDS_CUSTOMER_DATE_TIME = _("Не заданы поля customer_id, date, time")
