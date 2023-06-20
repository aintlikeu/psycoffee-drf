from django.contrib import admin
from django.urls import path, include
from accounts.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/login_user/', LoginView.as_view())
]
