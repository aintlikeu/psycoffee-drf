from django.contrib.auth import login, logout
from rest_framework import permissions, status, generics
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import Patient
from accounts.serializers import LoginSerializer, SignupSerializer, ProfileSerializer
from api.views.mixins import CustomSerializerByMethodMixin, CustomCreateMixin

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings


class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data, context={'request': self.request})
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({"success": True}, status=status.HTTP_202_ACCEPTED)


class LogoutView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        logout(request)
        return Response({"success": True}, status=status.HTTP_200_OK)


class SignupView(CustomSerializerByMethodMixin,
                 CustomCreateMixin,
                 generics.GenericAPIView):

    queryset = Patient.objects.all()

    serializer_map = {
        'POST': SignupSerializer
    }

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        # make user log in if account was created
        if response.status_code == 201:
            user = self.queryset.get(phone=request.data.get("phone"))
            login(request, user)
            return Response({"success": True}, status=status.HTTP_201_CREATED)
        else:
            return response


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

class GoogleLoginView(SocialLoginView):
    authentication_classes = []
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3002"
    client_class = OAuth2Client