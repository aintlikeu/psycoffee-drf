from django.urls import path

from accounts.views import LoginView, LogoutView, SignupView

urlpatterns = [
    path('login_user/', LoginView.as_view(), name='login'),
    path('logout_user/', LogoutView.as_view(), name='logout'),
    path('signup_user/', SignupView.as_view(), name='signup')
]
