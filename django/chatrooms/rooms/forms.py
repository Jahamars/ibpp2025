from django import forms
from .models import Room

class RoomCreationForm(forms.ModelForm):
    # Добавляем поле для подтверждения пароля, которого нет в модели
    password_confirm = forms.CharField(
        label="Подтвердите пароль", 
        widget=forms.PasswordInput
    )

    class Meta:
        model = Room
        # Указываем, какие поля из модели Room нужно показать в форме
        fields = ['name', 'password', 'password_confirm', 'max_users', 'encryption_algorithm']
        # Используем виджеты, чтобы сделать поля ввода красивее или функциональнее
        widgets = {
            'password': forms.PasswordInput(),
        }

    # Дополнительная проверка: пароли должны совпадать
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")
        
        return cleaned_data