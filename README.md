Тестовое задание REST API для системы комментариев блога
=====

Описание проекта
----------
Проект разворачивается в трех Docker контейнерах: web-приложение, postgresql-база данных и nginx-сервер.

Системные требования
----------
* Python 3.6+
* Docker
* Works on Linux, Windows, macOS, BS

Стек технологий
----------
* Python 3.8
* Django 3.1
* Django Rest Framework
* PostreSQL
* Nginx
* gunicorn
* Docker

Установка проекта из репозитория (Linux и macOS)
----------
1. Клонировать репозиторий и перейти в него в командной строке:
```bash 
git clone 'https://github.com/NikitaChalykh/test_work.git'

cd test_work
```

2. Cоздать и открыть файл ```.env``` с переменными окружения:
```bash 
cd infra

touch .env
```

3. Заполнить ```.env``` файл с переменными окружения по примеру (SECRET_KEY см. в файле ```settnigs.py```):
```bash 
echo DB_ENGINE=django.db.backends.postgresql >> .env

echo DB_NAME=postgres >> .env

echo POSTGRES_PASSWORD=postgres >> .env

echo POSTGRES_USER=postgres  >> .env

echo DB_HOST=db  >> .env

echo DB_PORT=5432  >> .env

echo SECRET_KEY=************ >> .env
```

4. Установка и запуск приложения в контейнерах (контейнер web загружактся из DockerHub):
```bash 
docker-compose up -d
```

5. Запуск миграций, создание суперюзера и сбор статики:
```bash 
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser

docker-compose exec web python manage.py collectstatic --no-input 
```
Документация к проекту
----------
Документация для API после установки доступна по адресу ```/redoc/```.
