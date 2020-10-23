from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User, UserLoginHistory, BankDetails


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def save(self):
        user = User(username = self.validated_data['username'])
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user

class GoogleLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class UserLoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginHistory
        fields = '__all__'


class BankDetailsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = BankDetails
        fields = '__all__'