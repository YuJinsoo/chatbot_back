from django.urls import path
from .views import Login, Logout, CreateUser

app_name="account"

urlpatterns = [
	path('login/', Login.as_view(), name='login'),
	path('logout/', Logout.as_view(), name='logout'),
	path('create/', CreateUser.as_view(), name='create'),
]