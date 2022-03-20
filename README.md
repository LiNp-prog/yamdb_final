![Django and Flake8 tests](https://github.com/LiNp-prog/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
![Build and Deploy](https://github.com/LiNp-prog/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Описание проекта:

Командный проект api_yamdb представляет из себя бэкэнд и api сервиса по публикации произведений с возможностью их оценивания.

### Над проектом работали:
  + Глеб Заровецкий
  + Сергей Никитин
  + Кузнецов Андрей

### Используемые технологии:

  + Django
  + Django REST framework
  + Docker
  + gunicorn
  + Nginx
  + Postgres
  + Python

### Шаблон заполнения env-файла:

Клонировать репозиторий и перейти в него в командной строке:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres #your password
DB_HOST=db
DB_PORT=5432
EMAIL_PASSWORD=password #your email password
```

### Описание команд для запуска приложения в контейнерах:

Зайдите в папку infra и выполните команды:

```
Пересоберите контейнеры и запустите их
    docker-compose up -d --build
Примените миграции
    docker-compose exec web python manage.py migrate
Создайте суперпользователя
    docker-compose exec web python manage.py createsuperuser
Соберите статику
    docker-compose exec web python manage.py collectstatic --no-input
Заполните базу данными
    docker-compose exec web python manage.py loaddata fixtures.json
```
