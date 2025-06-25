
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import RoomCreationForm
from .models import Room, Message

# Ваша функция для генерации ключа (пока заглушка)
def generate_encryption_key(algorithm):
    # !!! ВАЖНО: Здесь должна быть интеграция с вашей крипто-частью !!!
    # Например:
    # if algorithm == 'magma':
    #     return_key = get_magma_key()
    # else:
    #     return_key = get_kuznechik_key()
    return "dummy_secure_key_12345" # Временная заглушка

def create_room_view(request):
    if request.method == 'POST':
        # Если форма была отправлена (метод POST)
        form = RoomCreationForm(request.POST)
        if form.is_valid():
            #1. Дбавляем имя пользователя в форму
            username = form.cleaned_data['username']
            room = form.save(commit=False)
            # 2. Хешируем пароль перед сохранением
            room.password = make_password(form.cleaned_data['password'])
            # 3. Генерируем ключ шифрования
            room.encryption_key = generate_encryption_key(room.encryption_algorithm)
            
            # 4. Назначаем модератора (TO Do)
            # if request.user.is_authenticated:
            #     room.moderator = request.user

            # 5. сохранение в БД
            room.save()
            
            # 7. "ЛОГИНИМ" ПОЛЬЗОВАТЕЛЯ - сохраняем его имя в сессию
            request.session['username'] = username
            return redirect('chat_room', room_name=room.name) # 'chat_room' - имя URL

    else:
        form = RoomCreationForm()

    # Отображаем страницу, передавая в нее пустую или заполненную форму
    return render(request, 'rooms/create-room.html', {'form': form})


def join_room_view(request):
    if request.method == 'POST':
        room_name = request.POST.get('room-name')
        username = request.POST.get('username')
        password = request.POST.get('room-password')
        
        try:
            room = Room.objects.get(name=room_name)


            if check_password(password, room.password): # Проверяем хешированный пароль

                request.session['username'] = username # Сохраняем имя в сессию

                return redirect('chat_room', room_name=room.name)
            else:
                # Обработка ошибки "неверный пароль"
                pass
        except Room.DoesNotExist:
               # Обработка ошибки "комната не найдена"
           
            messages.error(request, 'Неверное название комнаты или пароль.')
            return redirect('landing_page') # Возвращаем на главную
    # Если что-то пошло не так, возвращаем на главную
    return redirect('landing_page') # Предполагается, что у вас есть URL с именем 'landing_page'
# View для главной страницы (index.html)
def landing_page_view(request):
    # Эта view просто отображает ваш index.html
    return render(request, 'rooms/index.html') 

# View-заглушка для комнаты чата
def chat_room_view(request, room_name):

    
    # Пока просто вернем текстовый ответ, чтобы убедиться, что редирект работает
    room = get_object_or_404(Room, name=room_name)

    if request.method == 'POST':
        # Если пришел POST-запрос, значит, пользователь отправил сообщение
        content = request.POST.get('content', '').strip()
        
        # TODO: Получить имя пользователя. Пока используем заглушку.
        # В будущем имя пользователя нужно будет брать из сессии после входа.
        username = request.session.get('username', 'Anonymous') 

        if content:
            # TODO: Здесь будет происходить ШИФРОВАНИЕ текста `content`
            # перед сохранением в базу данных.
            encrypted_content = content # Пока оставляем как есть

            Message.objects.create(
                room=room, 
                username=username, 
                content=encrypted_content
            )
    messages = room.messages.all()
    return render(request, 'rooms/chat.html', {
        'room': room,
        'messages': messages
    })