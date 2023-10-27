from rest_framework import serializers

from files.models import File


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'file', 'uploaded_at')
        model = File
