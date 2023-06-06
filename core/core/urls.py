from django.contrib import admin
from django.urls import path, include
# from api.routers import router
from api.views.patients import PatientRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register_user', PatientRegisterView.as_view()),
]
