from rest_framework import serializers
# django에서 제공하는 기본 password validation
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator # 중복 검사

from rest_framework.authtoken.models import Token # 토큰 모델
from django.contrib.auth import authenticate
from django.utils import timezone

from .models import Account


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Account.objects.all())])
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    password2 = serializers.CharField(write_only=True,required=True, validators=[validate_password])
    
    class Meta():
        model = Account
        fields = '__all__'
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password':'비밀번호가 일치하지 않습니다.'})
        
        return attrs
    
    def create(self, validated_data):
        user = Account.objects.create(
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user) # 토큰생성
        return user


class LoginSerializer(serializers.ModelSerializer):
    pass