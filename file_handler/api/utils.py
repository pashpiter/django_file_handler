# from PIL import Image
# from io import BytesIO


def validate_type(file):
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'application/rtf',
                     'application/pdf', 'application/msword', 'text/plain',
                     'text/csv', 'audio/mpeg', 'video/mp4']
    return file.content_type in allowed_types


def image_processing(file):
    # img = Image.open(file)
    # if img.format != 'JPEG':
    #     img = img.convert('RGB')
    # output = BytesIO()
    # img.save(output, format='JPEG', quality=quality)
    pass


def text_processing(file):
    pass


def audio_processing(file):
    pass


def video_processing(file):
    pass
