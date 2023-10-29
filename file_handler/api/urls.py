from django.urls import path
from .views import FileHandlerView, PingView


urlpatterns = [
    path('', PingView.as_view(), name='ping'),
    path('upload/',
         FileHandlerView.as_view({'post': 'create'}),
         name='upload'),
    path('files/', FileHandlerView.as_view({'get': 'list'}), name='file_list')
]
