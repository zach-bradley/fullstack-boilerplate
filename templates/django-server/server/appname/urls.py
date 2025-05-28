from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import UserRegistrationView, UserProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', UserRegistrationView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/profile/', UserProfileView.as_view(), name='profile'),
]
