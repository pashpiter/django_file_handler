docker run -d -p 5672:5672 -p 15672:15672 --hostname my-rabbit --name some-rabbit -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password -e RABBITMQ_DEFAULT_VHOST=vhost rabbitmq:3-management


celery -A file_handler worker -l INFO
