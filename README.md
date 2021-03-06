# email_distribution_server
Python 3.6.5  
Django 1.11.13  
SQLite  

**Тестовое задание 1**

Файл с настройками: **email_distribution_server.settings.base**  
Файл с локальными настройками (подключения к БД, email серверу, SECRET KEY, ALLOW HOST и др.): **email_distribution_server.settings.developer**  

При запуске сервера или применения миграций необходимо добавить ключ **--settings=email_distribution_server.settings.developer** или установить переменную окружения **DJANGO_SETTINGS_MODULE=email_distribution_server.settings.developer**

Ссылки:
	

 - Просмотр существующих эндпоинтов и возможность выполнения запросов к API через Swagger: /swagger
	
 - Административная панель: /admin
	
 - Отписка от рассылки: /email/unsubscribe/{verification_hash} (verification_hash можно посмотреть в административной
 панели, модель Email)

Данные для входа в административную панель:

 - Логин: admin
 - Пароль: adminadmin

Формат json для добавления группы рассылки через API (/api/emails/):
```
{
  "name": "string"
}
```

Формат json для добавления электронной почты (подписка(boolean), группа подписки(id)) через API(/api/groups-emails/):
```
{
  "email": "string",
  "subscription": true,
  "group": 0
}
```

Формат json для добавления задачи через API(/api/periodic-tasks/):
```
{
   "name":  "string",
   "interval":  {
	   "every": 10,
	   "period": "minutes"
   },
   "enabled":  true,
   "group_emails":  0
}
```
Типы значений для аттрибута period: days, hours, minutes, seconds, microseconds.

Папка с тестами: /api/tests  
Команда для выполнения (нужно перейти в папку с проектом): py.test

Запуск celery и celery-beat для выполнения заданий по рассылке писем:
	

 - python.exe celery.exe -A email_distribution_server worker -P gevent
	
 - python.exe celery.exe -A email_distribution_server beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
