from django.db import models



from django.db import models
from django.contrib.auth.models import User # Используем стандартную модель пользователя Django
import uuid # Для генерации уникальных имен, если понадобится

class Room(models.Model):
    # Настройки, которые задает пользователь
    name = models.CharField(max_length=100, unique=True, verbose_name="Название комнаты")
    password = models.CharField(max_length=128, verbose_name="Пароль (хешированный)") # Никогда не храните пароль в открытом виде!
    max_users = models.PositiveIntegerField(default=10, verbose_name="Макс. участников")


    # Выбор алгоритма шифрования
    ALGORITHM_CHOICES = [
        ('magma', 'Магма (ГОСТ Р 34.12-2015)'),
        ('kuznechik', 'Кузнечик (ГОСТ Р 34.12-2015)'),
    ]
    encryption_algorithm = models.CharField(
        max_length=20,
        choices=ALGORITHM_CHOICES,
        default='kuznechik',
        verbose_name="Алгоритм шифрования"
    )

    # Системные поля
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="moderated_rooms")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    # expires_at = models.DateTimeField(...) # Здесь можно добавить поле для времени жизни комнаты

    # КЛЮЧ ШИФРОВАНИЯ! Хранится только на сервере.
    # Мы будем заполнять его программно, не через форму.
    encryption_key = models.CharField(max_length=256, blank=True)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    username = models.CharField(max_length=100) # Имя автора сообщения
    content = models.TextField() # Текст сообщения (зашифрованный)
    timestamp = models.DateTimeField(auto_now_add=True) # Время отправки


    def __str__(self):
        return self.name
    

    class Meta:
        ordering = ['timestamp'] # Сортируем сообщения по времени отправки