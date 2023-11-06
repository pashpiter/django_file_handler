from os.path import splitext

from rest_framework import serializers

from files.models import File


class FileSerializer(serializers.ModelSerializer):
    """Сериалайзер для Файлов"""

    processed = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        fields = ('id', 'file', 'uploaded_at', 'processed')
        model = File

    def validate(self, attrs):
        """Валидация атрибутов"""
        if ('Ё' or 'Ё' or 'ё') in attrs['file'].name:
            raise serializers.ValidationError(
                {'message': 'You can not use "ё" in filename'},
                code=400)
        prefix, postfix = splitext(attrs['file'].name)
        new_name = self.file_rename(prefix)
        attrs['file'].name = (new_name +
                              ('.jpeg' if postfix == '.png' else postfix))
        if File.objects.filter(
                        file='uploaded_files/'+attrs['file'].name).exists():
            raise serializers.ValidationError(
                {'message': 'This name of file is already exsists'},
                code=400)
        return attrs

    def file_rename(self, file_name: str) -> str:
        to_replace = '''!"#$%&'()*+,.-/:;<=>?@[]^`{|}~ йЙ'''
        replace_with = '_'*(len(to_replace)-2) + 'иИ'
        for i in range(len(to_replace)):
            file_name = file_name.replace(
                to_replace[i], replace_with[i])
        return file_name
