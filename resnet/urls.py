from django.urls import path, include
from .views import image_upload_view

urlpatterns = [
    path('upload/', image_upload_view, name='upload_image'),
]