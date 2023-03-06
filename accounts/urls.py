from unicodedata import name
from django.urls import path
from .views import admin_login,district_user_login, create_district_user  ,userlogout ,userList ,resetPassword


urlpatterns = [
    path("admin/login", admin_login, name='admin-login'),
    path("user/logout", userlogout, name='logout'),
    path("subadmin/login", district_user_login, name="distric-user-login"),
    path("create/districtuser", create_district_user, name="district-user-login"),
    path("users", userList, name="userList"),
    path("reset-password", resetPassword, name="reset-password"),
   
]