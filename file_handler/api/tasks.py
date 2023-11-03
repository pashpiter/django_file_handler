import time

from celery import Task, shared_task
from rest_framework.response import Response

from files.models import File


def processing_file(file):
    """Выбор функции в зависимости от типа файла"""
    allowed_types: dict[str: Task] = {
        'image/jpeg': image_processing,
        'image/jpg': image_processing,
        'image/png': image_processing,
        'text/plain': text_processing,
        'text/csv': text_processing,
        'audio/mpeg': audio_processing,
        'video/mp4': video_processing
    }
    if file.content_type not in allowed_types:
        return Response({'message': 'This type of file is not allowed'},
                        status=403)
    return allowed_types[file.content_type].delay(file.name)


@shared_task
def image_processing(filename):
    """Обработка изображений"""
    time.sleep(10)
    update_processed(filename)


@shared_task
def text_processing(filename):
    """Обработка текста"""
    time.sleep(10)
    update_processed(filename)


@shared_task
def audio_processing(filename):
    """Обработка аудио"""
    time.sleep(10)
    update_processed(filename)


@shared_task
def video_processing(filename):
    """Обработка видео"""
    time.sleep(10)
    update_processed(filename)


def update_processed(filename):
    """Обноление статуса после выболнения обработки"""
    File.objects.filter(file='uploaded_files/'+filename).update(
        processed=True)
