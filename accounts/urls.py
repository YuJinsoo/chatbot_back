from django.urls import path, include
from .views import Login, Logout, CreateUser, RegisterAPIView

app_name="accounts"

urlpatterns = [
    # path('', include('dj_rest_auth.urls')),
    # path("registration/", include("dj_rest_auth.registration.urls")),
	path('login/', Login.as_view(), name='login'),
	path('logout/', Logout.as_view(), name='logout'),
	path('create/', CreateUser.as_view(), name='create'),
	path('register/', RegisterAPIView.as_view())
]