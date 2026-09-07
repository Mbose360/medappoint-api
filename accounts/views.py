from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import RegisterSerializer
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
        