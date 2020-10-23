from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, Login, GoogleLoginViewSet, SignupViewSet, BankDetailsViewSet

router = DefaultRouter()
router.register('user', UserViewSet, 'user')
router.register('google_login', GoogleLoginViewSet, 'google_login')
router.register('signup', SignupViewSet, 'signup')
router.register('bank_details', BankDetailsViewSet, 'bank_details')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', Login.as_view(), name='login'),
]