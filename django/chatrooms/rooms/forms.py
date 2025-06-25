from django import forms
from .models import Room

class RoomCreationForm(forms.ModelForm):

    username = forms.CharField(
        label="Ваше имя", 
        max_length=100,
        help_text="Это имя будет отображаться в чате."
    )
    # Поле для подтверждения пароля
    password_confirm = forms.CharField(
        label="Подтвердите пароль", 
        widget=forms.PasswordInput
    )

    class Meta:
        model = Room
        fields = ['name', 'password', 'password_confirm', 'max_users', 'encryption_algorithm']
        widgets = {
            'password': forms.PasswordInput(),
        }

    # Проверка паролей
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")
        
        return cleaned_data