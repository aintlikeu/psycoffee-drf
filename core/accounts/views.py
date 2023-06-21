from django.contrib.auth import login, logout
from rest_framework import permissions, status
from rest_framework import views
from rest_framework.response import Response

from accounts.serializers import LoginSerializer


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
