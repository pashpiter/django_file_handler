from rest_framework import serializers

from files.models import File


class FileSerializer(serializers.ModelSerializer):

    processed = serializers.BooleanField(default=False)

    class Meta:
        fields = ('id', 'file', 'uploaded_at', 'processed')
        model = File
