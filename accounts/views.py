from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BaseAuthentication, TokenAuthentication
from rest_framework import generics

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token # 토큰 모델

from django.contrib.auth.mixins import LoginRequiredMixin

from chatbot_project import my_setting

from .serializers import RegisterSerializer, LoginSerializer

## auth를 확장된 모델을 가져오게 됩니다.
Account = get_user_model()


class Login(APIView):
    permission_classes = [AllowAny]
    # authentication_classes = [BaseAuthentication]
    
    def get(self, request):
        return Response()

    def post(self, request):
        if request.user.is_authenticated:
            return Response({'message':'you already login'})
        
        
        print(request.query_params)
        print(request.parsers)
        print('post1')
        print(request.data) # QueryDict
        print('post2')
        # print(request.POST['email'])
        # print(dict(request.data))
        email = request.POST['email']
        pw = request.POST['password']
        user = Account.objects.filter(email=email)
        print(user) # QuerySet
        
        if user:
            user = authenticate(request, username=email, password=pw)
            print(user)

            if user:
                print('login?')
                # login(request, user)
                return Response({'message':'login success!'}, status=status.HTTP_200_OK)
        
        return Response({'message':'login failed. wrong id or password'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # if not request.user.is_authenticated:
        #     return Response({'message':'you are not login'})
        
        # serializer = AccountSerializer(request.user)
        logout(request)
        return Response({'message': 'logout success'}, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Account.objects.all()
    serializer_class = RegisterSerializer


### RegisterView를 APIView로 개발.
class SignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        user = Account.objects.create(email=request.data['email'], password=request.data['password'])
        
        user.save()
        
        token = Token.objects.create(acoount=user)
        return Response({'Token': token.key})


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) # 유효성 검사
        # serializer에서 선언한 validate()호출?
        token = serializer.validated_data
        return Response({'Token': token.key}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        print(request.data)
        print(request.user)
        print(request.user.is_authenticated)
        print(request.user.is_anonymous)
        
        token = request.headers.get('Authorization', None)
        print(token)
        
        if token:
            print('token avail!')
            try:
                token_key = token.split()[1]
                token = Token.objects.get(key=token_key)
                print('사용자:', token.user.email, '로그아웃!')
                # user = token.user
                return Response({'logout':'true'})
            except:
                return Response({'error': 'Token is inavalid'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'logout':'true'}, status=status.HTTP_400_BAD_REQUEST)

### 

class RegisterAPIView(APIView):
    def post(self, requset):
        return Response({"bye": "bye"})
#     def post(self, request):
#         # serializer = AccountSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
            
#             #jwt 토큰 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response({
#                 "user": serializer.data,
#                 "message": "register success",
#                 "token": {
#                     "access": access_token,
#                     "refresh": refresh_token,
#                 },
#             }, status=status.HTTP_200_OK,)
            
#             # jwt토큰 => 쿠키에 저장
#             res.set_cookie("access", access_token, httponly=True)
#             res.set_cookie("refresh", refresh_token, httponly=True)
            
#             return res
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # 시리얼라이저를 사용해서 유저를 저장하고(=회원가입), jwt 토큰을 받아서 쿠키에 저장한다. 쿠키에 저장할 때 httponly=True 속성을 줬는데, 이는 JavaScript로 쿠키를 조회할 수 없게 하기 위한 것이다. 따라서 XSS로부터 안전해지는데, 대신 CSRF로부터 취약해져서 CSRF 토큰을 같이 사용해야 한다.


# class AuthAPIView(APIView):
#     # 유저 정보 확인
#     def get(self, request):
#         try:
#             # access token을 decode 해서 유저 id 추출 => 유저 식별
#             access = request.COOKIES['access']
#             payload= jwt.decode(access, my_setting.Django_SECRET_KEY, algorithms=['HS256'])
#             pk = payload.get('user_id')
#             user = get_object_or_404(Account, pk=pk)
#             serializer = AccountSerializer(instance=user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         except(jwt.exceptions.ExpiredSignatureError):
#             # 토큰 만료 시 토큰 갱신
#             data = {'refresh': request.COOKIES.get('refresh', None)}
#             serializer = TokenRefreshSerializer(data=data)
#             if serializer.is_valid(raise_exception=True):
#                 access = serializer.data.get('access', None)
#                 refresh = serializer.data.get('refresh', None)
#                 payload = jwt.decode(access, my_setting.Django_SECRET_KEY, algorithms=['HS256'])
#                 pk = payload.get('user_id')
#                 user = get_object_or_404(Account, pk=pk)
#                 serializer = AccountSerializer(instance=user)
#                 res = Response(serializer.data, status=status.HTTP_200_OK)
#                 res.set_cookie('access', access)
#                 res.set_cookie('refresh', refresh)
#                 return res
#             raise jwt.exceptions.InvalidTokenError
        
#         except(jwt.exceptions.InvalidTokenError):
#             # 사용 불가능한 토큰일 때
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#     # 로그인
#     def post(self, request):
#     	# 유저 인증
#         user = authenticate(
#             email=request.data.get("email"), password=request.data.get("password")
#         )
#         # 이미 회원가입 된 유저일 때
#         if user is not None:
#             serializer = AccountSerializer(user)
#             # jwt 토큰 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     "user": serializer.data,
#                     "message": "login success",
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
#             # jwt 토큰 => 쿠키에 저장
#             res.set_cookie("access", access_token, httponly=True)
#             res.set_cookie("refresh", refresh_token, httponly=True)
#             return res
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     # 로그아웃
#     def delete(self, request):
#         # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
#         response = Response({
#             "message": "Logout success"
#             }, status=status.HTTP_202_ACCEPTED)
#         response.delete_cookie("access")
#         response.delete_cookie("refresh")
#         return response