from celery import Task, shared_task
from django.shortcuts import get_object_or_404
from PIL import Image

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
    text_translate(file.file.path)
    update_processed(file)


@shared_task
def audio_processing(id: int) -> None:
    """Обработка аудио"""
    file = get_object_or_404(File, pk=id)
    update_processed(file)


@shared_task
def video_processing(id: int) -> None:
    """Обработка видео"""
    file = get_object_or_404(File, pk=id)
    update_processed(file)


def text_translate(path: str) -> None:
    """Перевод текста (работает только с интернетом)"""
    try:
        import translators as ts

        with open(path, encoding='utf-8') as f:
            data = f.readlines()
        for i in range(len(data)):
            if data[i] != '\n':
                data[i] = ts.translate_text(
                    data[i], translator='google', to_language='ru')
            else:
                data[i] == '\n'
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(data))
    except Exception as e:
        raise e


def update_processed(file: File) -> None:
    """Обноление статуса после выболнения обработки"""
    file.processed = True
    file.save()
