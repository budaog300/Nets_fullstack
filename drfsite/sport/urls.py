from .views import *
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "sport"

router = routers.SimpleRouter()
router.register(r'sports', SportTypesViewSet, basename='sports')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'clubs', ClubsViewSet, basename='clubs')
router.register(r'veterans', VeteransViewSet, basename='veterans')


urlpatterns = [
    path('api/v1/', include(router.urls)),
    # path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


]