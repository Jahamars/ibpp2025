from django.urls import path
from . import views  # Импортируем views из ЭТОГО же приложения

urlpatterns = [
    # Путь для главной страницы (http://127.0.0.1:8000/)
    path('', views.landing_page_view, name='landing_page'),

    # Путь для страницы создания комнаты (http://127.0.0.1:8000/create-room/)
    path('create-room/', views.create_room_view, name='create-room'),

    
    path('join/', views.join_room_view, name='join-room'),

    # Путь для самой комнаты чата (например, http://127.0.0.1:8000/room/test-room/)
    path('room/<str:room_name>/', views.chat_room_view, name='chat_room'),
]