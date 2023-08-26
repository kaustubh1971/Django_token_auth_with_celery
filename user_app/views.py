# from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth import login, logout
# from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from user_app.serializer import UserLoginSerializer, UserRegistrationSerializer, UserSerializer
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
# from .validations import custom_validation, validate_email, validate_password
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from .tasks import test_func

class UserRegistration(APIView):
    permissions = (permissions.AllowAny,)

    def post(self, request):
        # clean_data = custom_validation(request.data)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print("serializer", serializer.data)
            user = serializer.create(request.data)
            if user:
                return Response({"email": user.email}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        # return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permissions = (permissions.AllowAny,)
    authentication_class = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        # assert validate_email(data)
        # assert validate_password(data)
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            try:
                user_token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                raise ValidationError("User doesn't have authentication details")
            return Response({"user_details": serializer.data, "token": user_token.key}, status=status.HTTP_200_OK)

class UserLogout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


def test(request):
    test_func.delay()
    # return Response({"Done"}, status=status.HTTP_200_OK)
    return HttpResponse("Done")
