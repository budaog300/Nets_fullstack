from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm

from .models import *


class LoginUserForm(AuthenticationForm):
    """ Форма авторизации """
    username = forms.CharField(max_length=100,
                               label_suffix="",
                               label="Логин",
                               widget=(
                                   forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин или E-mail'})))
    password = forms.CharField(label_suffix="",
                               label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    """ Форма регистрации """
    email = forms.EmailField(
        required=True, label_suffix="", label="Email",
        error_messages={'invalid': ''}
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():  # __iexact - воспринимает любой регистр за один
            raise forms.ValidationError("Такой Логин уже существует!")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2


class UpdateProfileUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин',
                               disabled=True,
                               widget=(
                                   forms.TextInput(attrs={'class': 'form-input'})))
    email = forms.CharField(label='Email',
                            disabled=True,
                            widget=(
                                forms.TextInput(attrs={'class': 'form-input'})))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'photo', 'date_birth']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }


class CustomPasswordRestForm(PasswordResetForm):
    """ Форма сброса пароля """

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь не найден')
        return email
