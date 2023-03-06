from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path("reports/", include('reports.urls')),
    path('V1/api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('V1/api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
