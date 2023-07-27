from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from django.contrib.auth.mixins import LoginRequiredMixin

from .serializers import AccountSerializer


class Registration(APIView):
    pass


class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        if request.user.is_authenticated:
            return Response({'message':'you already login'})
        
        user = authenticate(username=request.POST['email'], password=request.POST['password'])
        
        if user :
            login(request, user)
            return Response({'message':'login success!'})
        
        return Response({'message':'login failed. wrong id or password'})
        
        
class Logout(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = AccountSerializer(request.user)
        logout(request)
        return Response(serializer.data)