import mimetypes
import os
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from api.tasks import (audio_processing, image_processing, text_processing,
                       update_processed, video_processing)
from file_handler.settings import BASE_DIR
from files.models import File

TEMP_MEDIA_ROOT = tempfile.mkdtemp(BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class CeleryTasksTest(TestCase):
    """Тесты для celery tasks"""

    @classmethod
    def tearDownClass(cls):
        """Удаление временных файлов после выполнения тестов"""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True,)

    def test_image_processing(self):
        """Проверка обработки изображения"""
        path = os.path.join(BASE_DIR, 'tests/logo_apple_jpg.jpeg')
        filesize_before_processing = os.stat(path).st_size
        with open(path, 'rb') as f:
            img = SimpleUploadedFile('test.png', f.read(), 'image/jpeg')
            test_file = File.objects.create(file=img)
        image_processing(test_file.id)
        filesize_after_processing = os.stat(test_file.file.path).st_size
        with open(test_file.file.path) as f:
            self.assertLess(filesize_after_processing,
                            filesize_before_processing)

    def test_text_processing(self):
        """Проверка обработки текста"""
        f = SimpleUploadedFile('test.txt', b'test content', 'text/plain')
        test_file = File.objects.create(file=f)
        text_processing(test_file.id)
        with open(test_file.file.path) as f:
            text = f.read()
        self.assertEqual(text, 'тестовый контент')

    def test_video_processing(self):
        """Проверка обработки видео"""
        f = SimpleUploadedFile('test_video.mp4', b'test content', 'video/mp4')
        test_file = File.objects.create(file=f)
        video_processing(test_file.id)
        mt = mimetypes.guess_type(test_file.file.path)
        self.assertEqual(mt[0], 'video/mp4')

    def test_audio_processingo(self):
        """Проверка обработки аудио"""
        f = SimpleUploadedFile('test_audio.mp3', b'test content', 'audio/mpeg')
        test_file = File.objects.create(file=f)
        audio_processing(test_file.id)
        mt = mimetypes.guess_type(test_file.file.path)
        self.assertEqual(mt[0], 'audio/mpeg')

    def test_update_processing(self):
        """Проверка обработки поля processed после окончания обработки"""
        f = SimpleUploadedFile('test_processed.txt', b'test content',
                               'text/plain')
        test_file = File.objects.create(file=f)
        processed_before = test_file.processed
        update_processed(test_file)
        self.assertNotEqual(processed_before, test_file.processed)
