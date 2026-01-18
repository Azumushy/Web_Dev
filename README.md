# README

# Веб-приложение: система аутентификации и поиска

## Кратко

Простой монолит на Django + DRF с фронтендом на HTML/CSS/JS и SQLite по умолчанию. Реализованы регистрация, вход, выход, поиск пользователей и привязка JWT (access/refresh) к IP клиента.

## Стек

* Python 3.10+
* Django 6.x
* Django REST Framework
* djangorestframework-simplejwt
* SQLite (по умолчанию)
* HTML / CSS / JavaScript (клиент)

## Функционал

* Регистрация пользователя (email, пароль, подтверждение пароля, username, имя, фамилия)
* Валидация данных на клиенте и на сервере
* Вход по email/паролю
* Аутентификация через JWT (access + refresh)
* Логаут (blacklist refresh)
* Поиск пользователей по username, email, first_name, last_name
* Уровни доступа: гость, авторизованный пользователь, администратор
* Привязка токенов к IP клиента (проверка при запросах)

## Структура (основные файлы)

```
core/
  __init__.py
  asgi.py
  settings.py
  urls.py
  wsgi.py
  __pycache__/
    ...
users/
  __init__.py
  admin.py
  apps.py
  models.py
  serializers.py
  urls.py
  views.py
  views_pages.py
  authentication.py
  migrations/
    ...
  __pycache__/
    ...
templates/
  register.html
  login.html
  search.html
static/
  js/auth.js
  js/search.js
db.sqlite3
manage.py
README.md #(читаете)
```

## Установка (локально)

```bash
git clone https://github.com/Azumushy/Web_Dev.git
cd Final_project
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install --upgrade pip
pip install django djangorestframework djangorestframework-simplejwt    #необходимо для работы кода
```

Настройка `settings.py` (по умолчанию уже подходит для разработки):

* `AUTH_USER_MODEL = 'users.User'`
* `TEMPLATES['DIRS'] = [BASE_DIR / 'templates']`
* `STATIC_URL = 'static/'`
* `STATICFILES_DIRS = [BASE_DIR / 'static']`

Миграции и суперпользователь:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Открой:

* `http://127.0.0.1:8000/register/`
* `http://127.0.0.1:8000/login/`
* `http://127.0.0.1:8000/search/` (требует авторизации)

## API

Префикс: `/api/`

### POST /api/register/

Тело (JSON):

```json
{
  "username": "login123",
  "email": "user@example.com",
  "first_name": "Имя",
  "last_name": "Фамилия",
  "password": "пароль",
  "password2": "пароль"
}
```

Ответы:

* `201 Created` — пользователь создан
* `400 Bad Request` — ошибки валидации

### POST /api/login/

Тело:

```json
{
  "email": "user@example.com",
  "password": "пароль"
}
```

Ответ:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

Токены содержат поле `ip` с IP клиента.

### POST /api/logout/

Тело:

```json
{ "refresh": "<refresh_token>" }
```

Ответы:

* `205` или `200` — успешно
* `400` — неверный токен

### GET /api/search/?q=строка

Требует заголовок: `Authorization: Bearer <access>`
Возвращает список пользователей в формате:

```json
[
  {"username":"login","email":"user@example.com","first_name":"Имя","last_name":"Фамилия"}
]
```

## Привязка токена к IP и как её тестировать

* При логине в payload токена записывается `ip`:

  ```python
  refresh['ip'] = request.META.get('REMOTE_ADDR')
  ```
* Кастомная аутентификация сравнивает IP из токена и `REMOTE_ADDR`. При несовпадении возвращается `401`.

Проверка:

1. Авторизуйтесь в одном браузере, получите access и убедитесь, что поиск работает.
2. В другом браузере/устройстве вручную положите тот же `access` в `localStorage` и сделайте запрос к `/search/` — сервер должен вернуть 401.
3. Через `curl` с разного IP (VPN/мобильный интернет) тоже ожидается отказ.

**Примечание:** жёсткая привязка по IP защищает токены, но может мешать пользователям с меняющимся IP (мобильный интернет). Для реального продакшна можно сделать проверку мягче (сравнивать по стране или user-agent).

## Валидация и обработка ошибок

* Сериализаторы DRF проверяют входные данные
* Клиент делает базовую проверку (совпадение паролей)
* Сервер возвращает 400 с описанием ошибок при некорректных данных

## Уровни доступа

* Гость: может открывать страницы регистрации/логина
* Авторизованный: доступ к поиску и прочим защищённым эндпоинтам
* Администратор: superuser в `/admin/`

## Рекомендации и безопасность

* В продакшн используйте PostgreSQL и HTTPS
* Храните `SECRET_KEY` и другие секреты в переменных окружения
* Если фронтенд и бэкенд на разных доменах — добавьте `django-cors-headers`
* Подумайте о гибком подходе к проверке по IP, если пользователи часто меняют сеть

## Частые проблемы

* 404 при `/register.html` — маршруты настроены как `/register/`, `/login/`, `/search/`
* 401 с сообщением про IP — токен привязан к другому IP

## Возможные улучшения (необязательно)

* Перенести БД на PostgreSQL
* Сделать фронтенд на React/Vue с компонентным подходом
* Добавить поле `role` и гибкие права доступа
* Более гибкая проверка местоположения (страна, user-agent)

## Лицензия

Проект для учебных целей.
