"""
URL configuration for drfsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('sport/', include('sport.urls', namespace="sport")),
    path('users/', include('users.urls', namespace="users")),
    # path('api/v1/drf-auth/', include('rest_framework.urls')),

    # path('api/v1/clubs/', ClubsAPIList.as_view(), name='clubs-list'),
    # path('api/v1/clubs/<int:pk>/', ClubsAPIUpdate.as_view(), name='clubs-update'),
    # path('api/v1/clubs/<int:pk>/delete/', ClubsAPIDestroy.as_view(), name='clubs-delete'),
    # path('api/v1/sportlist/', SportTypesAPIView.as_view()),
    # path('api/v1/sportlist/<int:pk>/', SportTypesAPIView.as_view()),
    # path('api/v1/clubs/', ClubsAPIList.as_view()),
    # path('api/v1/clubs/<int:pk>/', ClubsAPIUpdate.as_view()),
    # path('api/v1/clubdetail/<int:pk>/', ClubsAPIDetailView.as_view()),
    # path('api/v1/clubs/', ClubsViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('api/v1/clubs/<int:pk>/', ClubsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('', RedirectView.as_view(url='/sport/', permanent=True)),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
