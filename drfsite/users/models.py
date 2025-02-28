from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """ Таблица Пользователи """
    username = models.CharField(max_length=255, unique=True, verbose_name="Логин")
    password = models.CharField(max_length=255, unique=False, verbose_name="Пароль")
    last_login = models.DateTimeField(auto_now=True, verbose_name="Последнее время вхождения")
    is_superuser = models.BooleanField(default=False, verbose_name="Superuser")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Email")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Аватарка")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    first_name = models.CharField(max_length=255, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=255, blank=True, verbose_name="Фамилия")
    date_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

    def __str__(self):
        return self.username
