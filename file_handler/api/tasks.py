import time

from celery import Task, shared_task
from rest_framework.response import Response

from files.models import File


def processing_file(content_type: str, id: int) -> Task:
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
    if content_type not in allowed_types:
        return Response({'message': 'This type of file is not allowed'},
                        status=403)
    return allowed_types[content_type].delay(id)


@shared_task
def image_processing(id: int) -> None:
    """Обработка изображений"""
    time.sleep(10)
    update_processed(id)


@shared_task
def text_processing(id: int) -> None:
    """Обработка текста"""
    time.sleep(10)
    update_processed(id)


@shared_task
def audio_processing(id: int) -> None:
    """Обработка аудио"""
    time.sleep(10)
    update_processed(id)


@shared_task
def video_processing(id: int) -> None:
    """Обработка видео"""
    time.sleep(10)
    update_processed(id)


def update_processed(id: int, new_file) -> None:
    """Обноление статуса после выболнения обработки"""
    File.objects.filter(pk=id).update(processed=True)
