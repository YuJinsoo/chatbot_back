from django.contrib import admin
from .models import Account

# Register your models here.
# admin.site.register(Account)

from django.contrib.auth.admin import UserAdmin

# 단일 요소는 반드시 쉼표가 있어야 합니다.
@admin.register(Account)
class CustomUserAdmin(UserAdmin):
    fieldsets = [
        ('프로필', {'fields': ('email', 'password')}),
        ('개인정보', {'fields': ('first_name', 'last_name')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('로그인정보', {'fields': ('last_login', 'date_joined')}),
    ]
    add_fieldsets = [
        ('프로필', {'fields': ('email', 'password1', 'password2')}),
    ]
    list_display = ('email', 'is_staff')
    ordering = ('email',)

# <class 'accounts.admin.CustomUserAdmin'>: (admin.E033) The value of 'ordering[0]' refers to 'username', which is not a field of 'accounts.Account'.
# 이 에러가 발생하는데 ordering을 뭘로할지 필요하단 이야기였음...
# username을 id로 안 쓰고 email로 쓰게 만들었기 때문에...