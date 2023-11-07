# django_file_handler


##### Стек: Python, Django, Postgresql, Celery, Pillow, Docker, nginx
***

### Что умеет django_file_handler
Приложение позволяет загрузить файлы на сервер, которые будут проходить обработку асинхронно.
Доступные виды обработки: перевод текста на русский (для текста), сжатие качества картинки (для изображений). 
Статус обработки можно проверить, по команде "Получение списка загруженных файлов".

### Запуск проекта

Для запуска проекта необходимо: 
* Клонировать репозиторий
```
git clone https://github.com/pashpiter/django_file_handler.git
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
```
curl "http://localhost/"
```
* Загрузка файла на сервер
```
POST http://localhost/upload/
Content-Type: multipart/form-data
```
```
curl -X POST "http://localhost/upload/" \
-H "Content-Type: multipart/form-data" \
-F "file=@{filepath}"
```
* Получение списка загруженных файлов
```
GET http://localhost/files/
```
```
curl "http://localhost/files/"
```

##### Доступ к админке
* Команда для создания админа-пользователя
```
sudo docker-compose exec app python manage.py createsuperuser
```
* Админка доступна по адресу
```
http://localhost/admin/
```

#### Pavel Drovnin [@pashpiter](http://t.me/pashpiter)
