from django.contrib import admin

from .models import CustomUser, Profile


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_staff', 'is_admin', 'is_director', 'is_manager', 'is_superuser', 'is_counter_staff']


admin.site.register(CustomUser, CustomUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'address', 'phone_number']


admin.site.register(Profile, ProfileAdmin)
