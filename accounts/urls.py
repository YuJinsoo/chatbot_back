from django.urls import path, include
from .views import Login, Logout, RegisterView, LoginView

app_name="accounts"

urlpatterns = [
    # path('', include('dj_rest_auth.urls')),
    # path("registration/", include("dj_rest_auth.registration.urls")),
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', Logout.as_view(), name='logout'),
	path('register/', RegisterView.as_view(), name='create'),
]