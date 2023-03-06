from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User ,Token


@admin.register(User)
class accounts(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + ((None, {'fields': ('is_district_user',)}),)

admin.site.register(Token)