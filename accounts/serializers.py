from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta():
        model = Account
        fields = '__all__'
        
    
    def create(self, validated_data):
        user = Account.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta():
        model = Account
        fields = ['email', 'password']