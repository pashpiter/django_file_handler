import os
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from rest_framework.response import Response

from file_handler.settings import BASE_DIR

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=os.path.join(BASE_DIR, 'tmp'))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class FileViewsTest(TestCase):
    """Тесты для View функций"""

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True,)

    def setUp(self) -> None:
        self.client = Client()

    def test_ping(self):
        response: Response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'app': 'django_file_handler',
                         'version': '1.0'})

    def test_post_empty_data(self):
        empty_data = {}
        response: Response = self.client.post('/upload/', data=empty_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'No file recieved')

    def test_post_image_file(self):
        with open(os.path.join(BASE_DIR, 'tests/apple.png'), 'rb') as f:
            data = {'file': f}
            response: Response = self.client.post('/upload/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['file'],
                         '/media/uploaded_files/apple.jpeg')

    def test_post_text_file(self):
        f = SimpleUploadedFile('test.txt', b'test content', 'text/plain')
        data = {'file': f}
        response: Response = self.client.post('/upload/', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['file'],
                         '/media/uploaded_files/test.txt')

    def test_invalid_post(self):
        f = SimpleUploadedFile('test.gif', b'test content', 'image/gif')
        data = {'file': f}
        response: Response = self.client.post('/upload/', data=data)
        self.assertEqual(response.status_code, 403)
        self.assertTrue('not allowed' in response.data['message'].lower())
