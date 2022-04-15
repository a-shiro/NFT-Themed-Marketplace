from django.contrib import admin

from DesertTraders.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'date_joined', 'last_login')
    sortable_by = ('is_staff', 'is_superuser', 'date_joined', 'last_login')