from http.client import responses
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model

User = get_user_model()


class SportTypesAPITests(APITestCase):
    """ Тесты для таблицы SportTypes """

    def setUp(self):
        self.category1 = Category.objects.create(name='Циклические')
        self.category2 = Category.objects.create(name='Единоборства')

        self.sport1 = SportTypes.objects.create(name='Бег', cat=self.category1)
        self.sport2 = SportTypes.objects.create(name='Дзюдо', cat=self.category2)

    def test_list(self):
        url = reverse('sport:sports-list')  # Замените на имя вашего URL
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        arr = SportTypes.objects.all()
        serializer = SportTypesSerializer(arr, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_retrieve(self):
        url = reverse('sport:sports-detail', args=[self.sport1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        url = reverse('sport:sports-list')
        data = {
            'name': 'Плаванье',
            'cat_id': '3'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        arr = SportTypes.objects.filter(name='Плаванье')
        self.assertTrue(arr.exists(), "'Плаванье' не найден")

    def test_put(self):
        url = reverse('sport:sports-detail', args=[self.sport1.id])
        data = {
            'name': 'Плаванье',
            'cat_id': '2'
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.sport1.refresh_from_db()
        arr = SportTypes.objects.filter(name='Плаванье')
        self.assertTrue(arr.exists(), "'Плаванье' не найден")

    def test_delete(self):
        url = reverse('sport:sports-detail', args=[self.sport1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SportTypes.objects.filter(id=self.sport1.id).exists(), "Спорт не был удален")


class CategoryAPITests(APITestCase):
    """ Тесты для таблицы Category """

    def setUp(self):
        self.cat1 = Category.objects.create(name='Игровые')
        self.cat2 = Category.objects.create(name='Циклические')

    def test_list(self):
        url = reverse('sport:category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        arr = Category.objects.all()
        serializer = CategorySerializer(arr, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_retrieve(self):
        url = reverse('sport:category-detail', args=[self.cat1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        url = reverse('sport:category-list')
        data = {
            'name': 'Единоборства',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        arr = Category.objects.filter(name='Единоборства')
        self.assertTrue(arr.exists(), "'Единоборства' не найден")

    def test_put(self):
        url = reverse('sport:category-detail', args=[self.cat1.id])
        data = {
            'name': 'Единоборства',
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cat1.refresh_from_db()
        arr = Category.objects.filter(name='Единоборства')
        self.assertTrue(arr.exists(), "'Единоборства' не найден")

    def test_delete(self):
        url = reverse('sport:category-detail', args=[self.cat1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.cat1.id).exists(), "Категория не был удален")


class ClubsAPITests(APITestCase):
    """ Тесты для таблицы Clubs """

    def setUp(self):
        self.director1 = Directors.objects.create(
            last_name='Иванов',
            first_name='Иван',
            patronymic='Иванович'
        )
        self.director2 = Directors.objects.create(
            last_name='Петров',
            first_name='Петр',
            patronymic='Петрович'
        )
        self.club1 = Clubs.objects.create(name='Клуб 1', address='Адрес 1', director=self.director1)
        self.club2 = Clubs.objects.create(name='Клуб 2', address='Адрес 2', director=self.director2)

    def test_list(self):
        url = reverse('sport:clubs-list')  # Замените на имя вашего URL
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        arr = Clubs.objects.all()
        serializer = ClubsSerializer(arr, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_retrieve(self):
        url = reverse('sport:clubs-detail', args=[self.club1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        url = reverse('sport:clubs-list')
        data = {
            'name': 'Клуб 3',
            'address': 'Адрес 3',
            'director': {
                'last_name': 'Петров',
                'first_name': 'Петр',
                'patronymic': 'Петрович'
            }
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        arr = Clubs.objects.filter(name='Клуб 3')
        self.assertTrue(arr.exists(), "'Клуб 3' не найден")

    def test_put(self):
        url = reverse('sport:clubs-detail', args=[self.club1.id])
        data = {
            'name': 'Клуб 4',
            'address': 'Адрес 4',
            'director': {
                'last_name': 'Петров',
                'first_name': 'Петр',
                'patronymic': 'Петрович'
            }
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.club1.refresh_from_db()
        arr = Clubs.objects.filter(name='Клуб 4')
        self.assertTrue(arr.exists(), "'Клуб 4' не найден")

    def test_delete(self):
        url = reverse('sport:clubs-detail', args=[self.club1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Clubs.objects.filter(id=self.club1.id).exists(), "Клуб не был удален")


class VeteransAPITests(APITestCase):
    """ Тесты для таблицы Veterans """

    def setUp(self):
        self.cat1 = Category.objects.create(name='Игровые')
        self.cat2 = Category.objects.create(name='Циклические')

        self.sport1 = SportTypes.objects.create(name='Волейбол', cat=self.cat1)
        self.sport2 = SportTypes.objects.create(name='Бег', cat=self.cat2)

        self.club1 = Clubs.objects.create(name='Клуб 1', address='Адрес 1')
        self.club2 = Clubs.objects.create(name='Клуб 2', address='Адрес 2')
        data = {
            'last_name': 'Иванов',
            'first_name': 'Иван',
            'patronymic': 'Иванович',
            'gender': 'male',
            'age_group': '60-69',

        }
        with open('media/veterans_photos/yanix.jpg', 'rb') as f:
            data['photo'] = SimpleUploadedFile(
                name='yanix.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )

        self.vet1 = Veterans.objects.create(**data)

    def test_list(self):
        url =  reverse('sport:veterans-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        url = reverse('sport:veterans-detail', args=[self.vet1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post(self):
        url = reverse('sport:veterans-list')
        data = {
            'last_name': 'Сидоров',
            'first_name': 'Сидор',
            'gender': 'male',
            'age_group': '60-69',
        }
        with open('media/veterans_photos/damn.jpg', 'rb') as f:
            data['photo'] = SimpleUploadedFile(
                name='damn.jpg',
                content=f.read(),
                content_type='image/jpeg'
            )
            response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        arr = Veterans.objects.filter(last_name='Сидоров')
        self.assertTrue(arr.exists(), "'Сидоров' не найден")

    def test_put(self):
        url = reverse('sport:veterans-detail', args=[self.vet1.id])
        data = {
            'last_name': 'Сидоров',
            'first_name': 'Сидор',
            'gender': 'female',
            'age_group': '60-69',
        }

        with open('media/veterans_photos/damn.jpg', 'rb') as f:
            data['photo'] = SimpleUploadedFile(
                name = 'damn.jpg',
                content = f.read(),
                content_type = 'image/jpeg'
            )
            response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        url = reverse('sport:veterans-detail', args=[self.vet1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Veterans.objects.filter(id=self.vet1.id).exists(), "Ветеран не был удален")