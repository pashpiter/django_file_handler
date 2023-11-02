from PIL import Image
from io import BytesIO
from rest_framework.response import Response
from celery import shared_task, Task
from file_handler.settings import BASE_DIR
import os
from files.models import File
import time


def processing_file(file):
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
    img = Image.open(
        os.path.join(BASE_DIR, 'media/uploaded_files/') + filename)
    if img.format != 'JPEG':
        img = img.convert('RGB')
    output = BytesIO()
    img.save(output, format='JPEG')
    time.sleep(10)
    update_processed.delay(filename)


@shared_task
def text_processing(filename):
    time.sleep(10)
    update_processed.delay(filename)


@shared_task
def audio_processing(filename):
    time.sleep(10)
    update_processed.delay(filename)


@shared_task
def video_processing(filename):
    time.sleep(10)
    update_processed.delay(filename)


@shared_task
def update_processed(filename):
    File.objects.filter(file='uploaded_files/'+filename).update(processed=True)
