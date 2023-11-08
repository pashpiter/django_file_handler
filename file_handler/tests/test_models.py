import os
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from file_handler.settings import BASE_DIR
from files.models import File

TEMP_MEDIA_ROOT = tempfile.mkdtemp(BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FileModelTests(TestCase):
    """Тесты для модели File"""

    @classmethod
    def setUpTestData(cls):
        """Добавление данных в БД"""
        f = SimpleUploadedFile('test.txt', b'test content', 'text/plain')
        cls.test_file = File.objects.create(file=f)
        cls.file_field = cls.test_file._meta.get_field('file')
        cls.uploaded_at_filed = cls.test_file._meta.get_field('uploaded_at')
        cls.processed_filed = cls.test_file._meta.get_field('processed')

    @classmethod
    def tearDownClass(cls):
        """Удаление временных файлов после выполнения тестов"""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True,)

    def test_file_verbose_name(self):
        """Проверка verbose_name у поля file"""
        real_verbose_name = getattr(self.file_field, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Имя файла')

    def test_file_upload_to(self):
        """Проверка параметра upload_to у поля file"""
        real_path = getattr(self.file_field, 'upload_to')
        self.assertEqual(real_path, 'uploaded_files/')

    def test_uploaded_at_verbose_name(self):
        """Проверка verbose_name у поля upload_at"""
        real_verbose_name = getattr(self.uploaded_at_filed, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Время загрузки')

    def test_uploaded_at_auto_now(self):
        """Проверка поля добавеления времени в автоматическом режиме"""
        real_auto_now = getattr(self.uploaded_at_filed, 'auto_now')
        self.assertTrue(real_auto_now)

    def test_processed_verbose_name(self):
        """Проверка verbose_name у поля processed"""
        real_verbose_name = getattr(self.processed_filed, 'verbose_name')
        self.assertEqual(real_verbose_name, 'Обработка')

    def test_processed_default(self):
        """Проверка дефолтного значения у поля processed"""
        real_deafult = getattr(self.processed_filed, 'default')
        self.assertEqual(real_deafult, False)
