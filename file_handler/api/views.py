from rest_framework import mixins, viewsets, views
from rest_framework.response import Response
from files.models import File
from .serializers import FileSerializer
from .tasks import processing_file
from rest_framework.parsers import MultiPartParser


class PingView(views.APIView):
    def get(self, request):
        return Response({'app': 'django_file_handler', 'version': '1.0'},
                        status=200)


class FileHandlerView(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response({'message': 'No file recieved'}, status=400)
        serializer = FileSerializer(File(), data=request.data)
        if serializer.is_valid():
            serializer.validated_data['processed'] = False
            serializer.save()
            processing_file(request.data.get('file'))
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def perform_create(self, serializer):
        return super().perform_create(serializer)
