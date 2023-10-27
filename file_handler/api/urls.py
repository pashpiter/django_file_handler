from django.urls import path
from .views import FileUploadHandler


urlpatterns = [
    path('upload/', FileUploadHandler.as_view({'post': 'create'}), name='upload')
]
