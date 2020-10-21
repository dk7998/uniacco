from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, Login, GoogleLoginViewSet

router = DefaultRouter()
router.register('user', UserViewSet, 'user')
router.register('google_login', GoogleLoginViewSet, 'google_login')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', Login.as_view(), name='login')
]