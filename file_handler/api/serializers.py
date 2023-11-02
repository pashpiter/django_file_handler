from rest_framework import serializers

from files.models import File


class FileSerializer(serializers.ModelSerializer):

    processed = serializers.BooleanField(default=False)

    class Meta:
        fields = ('id', 'file', 'uploaded_at', 'processed')
        model = File

    def validate(self, attrs):
        if ('Ё' or 'Ё' or 'ё') in attrs['file'].name:
            raise serializers.ValidationError(
                {'message': 'You can not use "ё" in filename'},
                code=400)
        to_replace = '''!"#$%&'()*+,-/:;<=>?@[\]^_`{|}~ йЙ'''
        replace_with = '_'*(len(to_replace)-2) + 'иИ'
        for i in range(len(to_replace)):
            attrs['file'].name = attrs['file'].name.replace(
                to_replace[i], replace_with[i])
        if File.objects.filter(
                        file='uploaded_files/'+attrs['file'].name).exists():
            raise serializers.ValidationError(
                {'message': 'This name of file is already exsists'},
                code=400)
        return super().validate(attrs)
