from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta():
        model = Account
        fields = ['email', 'password', 'name']
        
    
    def create(self, validated_data):
        user = Account.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            name = validated_data.get('name')
        )
        return user