from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import RegisterSerializer , LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class RegisterAPI(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            RegisterSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

class LoginAPI(APIView):
    def post(self, request):

        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]  
        refresh = RefreshToken.for_user(user)

        return Response(
            {            
                "refresh":str(refresh),
                "access": str(refresh.access_token),
                "user":{
                 "id": user.id,
                 "email":user.email,
                 "role": user.role,
                }
            },
            status=status.HTTP_200_OK

        )
