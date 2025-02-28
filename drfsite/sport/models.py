from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .utils import unique_slugify
import datetime


class SportTypes(models.Model):
    """ Таблица Виды спорта """
    name = models.CharField(max_length=255, verbose_name="Название спорта")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    cat = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name="Категории")

    def save(self, *args, **kwargs):
        if self.pk:  # Проверяем, что объект уже создан (существует в базе данных)
            original = SportTypes.objects.get(pk=self.pk)  # Получаем оригинальный объект из базы данных
            if original.name != self.name:
                self.slug = unique_slugify(self, self.name)  # Генерируем новый slug

        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sport:sport', kwargs={'sport_slug': self.slug})

    class Meta:
        verbose_name = 'Виды спорта'
        verbose_name_plural = 'Виды спорта'


class Category(models.Model):
    """ Таблица Категории видов спорта """
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sport:category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категории видов спорта'
        verbose_name_plural = 'Категории видов спорта'


class Clubs(models.Model):
    """ Таблица Клубы ветеранов спорта """
    name = models.CharField(max_length=100, verbose_name="Клуб ветеранов спорта")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    time_create = models.DateField(auto_now_add=True, verbose_name="Год основания")
    director = models.CharField(max_length=100, verbose_name="Руководитель клуба")
    address  = models.CharField(max_length=100, verbose_name="Адрес клуба")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sport:club', kwargs={'club_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клуб ветеранов спорта'
        verbose_name_plural = 'Клубы ветеранов спорта'


class Veterans(models.Model):
    """ Таблица Ветераны """
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    gender = models.CharField(max_length=100, choices=[('male', 'Мужской'), ('female', 'Женский')], verbose_name="Пол")
    age_group = models.CharField(max_length=100, verbose_name="Возрастная группа")
    sport = models.ForeignKey('SportTypes', on_delete=models.CASCADE, null=True, verbose_name="Вид спорта")
    photo = models.ImageField(upload_to="veterans_photos", verbose_name="Фото ветерана")
    club = models.ForeignKey('Clubs', on_delete=models.SET_NULL, null=True, verbose_name="Клуб ветеранов спорта")
    achievements = models.CharField(max_length=255, blank=True, null=True, verbose_name="Перечень наград")
    # achievements = models.JSONField(default=None, blank=True, null=True, verbose_name="Перечень наград")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.get_full_name())
        super().save(*args, **kwargs)

    def get_full_name(self):
        """ Возвращает полное имя в формате ФИО """
        return f"{self.last_name} {self.first_name} {self.patronymic}".strip()

    def get_absolute_url(self):
        return reverse('sport:veteran', kwargs={'veteran_slug': self.slug})

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Ветерана'
        verbose_name_plural = 'Ветераны'





