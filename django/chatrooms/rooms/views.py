
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .forms import RoomCreationForm, RoomUpdateForm
from .models import Room, Message


def generate_encryption_key(algorithm):
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

           
          
            
            request.session['username'] = username
            room.moderator_username = username 
             # сохранение в БД
            room.save()
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
    return redirect('landing_page') 
# View для главной страницы (index.html)
def landing_page_view(request):

    return render(request, 'rooms/index.html') 


def delete_room_view(request, room_name):
    if request.method == 'POST':
        room = get_object_or_404(Room, name=room_name)
        if request.session.get('username') == room.moderator_username:
            room.delete()
            messages.success(request, f"Комната '{room_name}' была успешно удалена.")
            return redirect('landing_page')
    return redirect('chat_room', room_name=room_name)

def leave_room_view(request, room_name):
    # Просто очищаем сессию и возвращаем на главную
    if 'username' in request.session:
        del request.session['username']
    messages.info(request, "Вы покинули комнату.")
    return redirect('landing_page')

def chat_room_view(request, room_name):
    # --- БЛОК 1: ПОДГОТОВКА ДАННЫХ (выполняется всегда) ---
    room = get_object_or_404(Room, name=room_name)
    current_user = request.session.get('username')
    is_moderator = (current_user == room.moderator_username)
    
    participants = set(room.messages.values_list('username', flat=True))
    if current_user:
        participants.add(current_user)
    participants_count = len(participants)
    
    # ИЗМЕНЕНИЕ: Получаем список сообщений ЗДЕСЬ, до всех проверок
    all_messages = room.messages.all()
    
    update_form = RoomUpdateForm()
    
    # --- БЛОК 2: ОБРАБОТКА POST-ЗАПРОСОВ ---
    if request.method == 'POST':
        if 'content' in request.POST:
            content = request.POST.get('content', '').strip()
            if content:
                Message.objects.create(
                    room=room, 
                    username=current_user or 'Anonymous', 
                    content=content
                )
            return redirect('chat_room', room_name=room.name)
            
        elif 'new_password' in request.POST and is_moderator:
            filled_update_form = RoomUpdateForm(request.POST)
            if filled_update_form.is_valid():
                new_pass = filled_update_form.cleaned_data['new_password']
                room.password = make_password(new_pass)
                room.save()
                messages.success(request, "Пароль комнаты успешно обновлен.")
                return redirect('chat_room', room_name=room.name)
            else:
                update_form = filled_update_form

    # --- БЛОК 3: ОТОБРАЖЕНИЕ СТРАНИЦЫ ---
    
    return render(request, 'rooms/chat.html', {
        'room': room,
        'messages': all_messages, # Используем переменную, определенную ранее
        'is_moderator': is_moderator,
        'participants_count': participants_count,
        'participants': list(participants),
        'update_form': update_form,
    })