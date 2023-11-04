from rest_framework import mixins, views, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response


from .serializers import FileSerializer
from .tasks import processing_file
from files.models import File

ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'text/plain',
                 'text/csv', 'audio/mpeg', 'video/mp4']


class PingView(views.APIView):
    """Класс для проверки работы приложения"""
    def get(self, request):
        return Response({'app': 'django_file_handler', 'version': '1.0'},
                        status=200)


class FileHandlerView(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """ViewsSet для создания и возврата списка файлов"""
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response({'message': 'No file recieved'}, status=400)
        if request.data['file'].content_type not in ALLOWED_TYPES:
            return Response({'message': 'This type of file is not allowed'},
                            status=403)
        serializer = FileSerializer(File(), data=request.data)
        if serializer.is_valid():
            serializer.validated_data['processed'] = False
            obj = serializer.save()
            processing_file(request.data.get('file').content_type, obj.id)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
