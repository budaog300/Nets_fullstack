from django.contrib.auth import authenticate
from django.forms import model_to_dict
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from pyexpat.errors import messages
from .models import *

# DRF
from rest_framework import generics, status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *


class ClubsAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000


class SingleObjectMixin:
    # pagination_class = ClubsAPIListPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, filters.SearchFilter]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if not pk:
            return self.queryset.all()
        return self.queryset.filter(pk=pk)


class RegisterView(APIView):
    """ Регистрация """
    def post(self, request):
        serializer = UsersTypesSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user) # Создание Refesh и Access
            refresh.payload.update({    # Полезная информация в самом токене
                'user_id': user.id,
                'username': user.username
            })
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token), # Отправка на клиент

            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """ Авторизация """
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if username is None or password is None:
            return Response({'error': 'Требуется указать имя пользователя и пароль'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'error': 'Неверные данные'},
                            status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    """ Выход из системы """
    def post(self, request):
        refresh_token = request.data.get('refresh_token') # С клиента нужно отправить refresh token
        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist() # Добавить его в чёрный список
        except Exception as e:
            return Response({'error': 'Неверный Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)


class Profile(APIView):
    """ Профиль """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UsersTypesSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = request.user

        # Создаем сериализатор для обновления данных
        serializer = UsersTypesSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # Сохраняем изменения
            serializer.save()

            # Если передан новый пароль, хешируем его
            if 'password' in request.data:
                user.set_password(request.data['password'])
                user.save()

            # Возвращаем обновленные данные пользователя
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Возвращаем ошибки валидации
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersTypesViewSet(SingleObjectMixin, viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersTypesSerializer
    filterset_fields = ['username', ]
    ordering_fields = ['username',]
    search_fields = ['username']




