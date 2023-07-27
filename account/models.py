from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class AccountManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        now = timezone.now() # 현재시간 -> UTC
        # now = timezone.localtime() # 현재 위치 시간으로 기록됨
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            is_staff = is_staff,
            is_active = True,
            is_superuser = is_superuser,
            last_login = now,
            date_joined = now
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
        
    # BaseUserManger함수 1 : create_user
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)
    
    # BaseUserManger함수 2 : create_superuser
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)



class Account(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=50, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateField(null=True, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    
    # User 모델의 필수 field, is_active, is_superuser
    is_active = models.BooleanField(default=True)    
    
    objects = AccountManager()
    
    USERNAME_FIELD = 'email'
    EMAIL_FILED = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f"email : {self.email}"