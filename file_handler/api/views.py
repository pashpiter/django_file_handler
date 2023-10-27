from rest_framework import pagination, mixins, viewsets
from files.models import File
from .serializer import FileSerializer


class FileUploadHandler(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileListHandler(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    pagination_class = pagination.PageNumberPagination
