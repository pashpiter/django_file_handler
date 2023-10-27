from django.db import models


class File(models.Model):
    file = models.FileField(verbose_name='Имя файла')
    uploaded_at = models.DateTimeField(verbose_name='Время загрузки',
                                       auto_now=True,)
    processed = models.BooleanField(verbose_name='Обработка')
