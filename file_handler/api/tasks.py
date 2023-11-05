import time

from celery import Task, shared_task
from django.shortcuts import get_object_or_404
from files.models import File
from PIL import Image
from rest_framework.response import Response


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
    pic = get_object_or_404(File, pk=id)
    img = Image.open(pic.file)
    if img.format != 'JPEG':
        img = img.convert('RGB')
    img.save(pic.file.path, format='JPEG', quality=70)
    update_processed(pic)


@shared_task
def text_processing(id: int) -> None:
    """Обработка текста"""
    file = get_object_or_404(File, pk=id)
    text_editing(file.file.path)
    update_processed(file)


@shared_task
def audio_processing(id: int) -> None:
    """Обработка аудио"""
    file = get_object_or_404(File, pk=id)
    time.sleep(10)
    update_processed(file)


@shared_task
def video_processing(id: int) -> None:
    """Обработка видео"""
    file = get_object_or_404(File, pk=id)
    time.sleep(10)
    update_processed(file)


def text_editing(path: str) -> None:
    with open(path, encoding='utf-8') as f:
        data = f.readlines()
    for i in range(len(data)):
        line = list(data[i])
        for j in range(len(line)):
            if line[j] == 'R':
                line[j] == 'Я'
            elif line[j] == ('B'):
                line[j] = 'Б'
        data[i] = ''.join(line)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(''.join(data))


def update_processed(file: File) -> None:
    """Обноление статуса после выболнения обработки"""
    file.processed = True
    file.save()
