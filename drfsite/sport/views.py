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
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from .filters import *


class ClubsAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000


class SingleObjectMixin:
    pagination_class = ClubsAPIListPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, filters.SearchFilter]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        if not pk:
            return self.queryset.all()
        return self.queryset.filter(pk=pk)


class SportTypesViewSet(SingleObjectMixin, viewsets.ModelViewSet):
    queryset = SportTypes.objects.all()
    serializer_class = SportTypesSerializer
    filterset_fields = ['name', 'cat']
    ordering_fields = ['name', 'cat']
    search_fields = ['name']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Название спорта", type=openapi.TYPE_STRING),
            openapi.Parameter('cat', openapi.IN_QUERY, description="Категория", type=openapi.TYPE_STRING),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CategoryViewSet(SingleObjectMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['name']
    ordering_fields = ['name']
    search_fields = ['name']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Категория", type=openapi.TYPE_STRING),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ClubsViewSet(SingleObjectMixin, viewsets.ModelViewSet):
    queryset = Clubs.objects.all()
    serializer_class = ClubsSerializer
    filterset_fields = ['name', 'address', 'time_create',]
    ordering_fields = ['name', 'director', 'time_create', 'address']
    search_fields = ['name']
    # permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Имя клуба", type=openapi.TYPE_STRING),
            openapi.Parameter('address', openapi.IN_QUERY, description="Адрес клуба", type=openapi.TYPE_STRING),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class VeteransViewSet(SingleObjectMixin, viewsets.ModelViewSet):
    queryset = Veterans.objects.all()
    serializer_class = VeteransSerializer
    filterset_class = VeteransFilter
    # filterset_fields = ['last_name', 'gender', 'age_group', 'sport', 'club', 'achievements']
    ordering_fields = ['last_name', 'gender', 'age_group', 'sport', 'club', 'achievements']
    ordering = ['last_name']
    search_fields = ['last_name']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('last_name', openapi.IN_QUERY, description="last_name", type=openapi.TYPE_STRING),
            openapi.Parameter('gender', openapi.IN_QUERY, description="gender", type=openapi.TYPE_STRING),
            openapi.Parameter('sport', openapi.IN_QUERY, description="sport", type=openapi.TYPE_STRING),
            openapi.Parameter('club', openapi.IN_QUERY, description="club", type=openapi.TYPE_STRING),
            openapi.Parameter('achievements', openapi.IN_QUERY, description="achievements", type=openapi.TYPE_STRING),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)





# class ClubsAPIList(generics.ListCreateAPIView):
#     queryset = Clubs.objects.all()
#     serializer_class = ClubsSerializer
#     pagination_class = ClubsAPIListPagination
#
#
# class ClubsAPIUpdate(generics.RetrieveUpdateAPIView):
#     queryset = Clubs.objects.all()
#     serializer_class = ClubsSerializer
#
#
# class ClubsAPIDestroy(generics.RetrieveDestroyAPIView):
#     queryset = Clubs.objects.all()
#     serializer_class = ClubsSerializer
#     # permission_classes = (IsAuthenticated,)
#

# class SportTypesAPIView(APIView):
#     def get(self, request):
#         s = SportTypes.objects.all()
#
#         return Response({'sports': SportTypesSerializer(s, many=True).data})
#
#     def post(self, request):
#         serializer = SportTypesSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'message': serializer.data}, 201)
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)  # идентификатор записи, по которому она выбирается из БД
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = SportTypes.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#
#         serializer = SportTypesSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'message': serializer.data}, 201)
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             instance = SportTypes.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#
#         instance.delete()
#
#         return Response({"message": "deleted post " + str(pk)})
