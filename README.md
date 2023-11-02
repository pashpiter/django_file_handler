# django_file_handler


##### Стек: Python, Django, Postgresql, Celery, Pillow, Docker, nginx
***

### Запуск проекта

Для запуска проекта необходимо: 
* Клонировать репозиторий
```
git clone git@github.com:pashpiter/django_file_handler.git
```
* Перейти в папку django_file_handler

* Запустить проект используя docker-compose
```
sudo docker-compose up -d
```

### Примеры команд API
* Проверка работы приложения
```
GET http://localhost/
```
* Загрузка файла на сервер
```
POST http://localhost/upload/
```
```
curl -X POST "http://localhost/upload/" \
-H "Content-Type: multipart/form-data" \
-F "file=@{filename}"
```
* Получение списка загруженных файлов
```
GET http://localhost/files/
```
```
curl "http://localhost/files/"
```

#### Pavel Drovnin [@pashpiter](http://t.me/pashpiter)
