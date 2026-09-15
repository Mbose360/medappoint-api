from rest_framework import serializers
from django.contrib.auth import authenticate

from accounts.models import User
from doctors.models import Doctor
from patients.models import Patient
from django.db import transaction

class RegisterSerializer(serializers.ModelSerializer):

    speciality = serializers.CharField(required=False)
    biography = serializers.CharField(required=False,allow_blank=True)
    location = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'role',
            'speciality',
            'biography',
            'location',
            'phone_number',
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        role = data.get("role")

        if role == 'DOCTOR':
            if not data.get("speciality"):
                raise serializers.ValidationError(
                    "Doctors must provide a speciality."
                )
            if not data.get("location"):
                raise serializers.ValidationError(
                    {"location": "Doctors must provide a location."}
                )    

        return data

    def create(self, validated_data):

        speciality = validated_data.pop("speciality", None)
        biography = validated_data.pop("biography", None)
        location = validated_data.pop("location", None)
        with transaction.atomic():

         user = User.objects.create_user(**validated_data)
   
         if user.role == "DOCTOR":
            Doctor.objects.create(
               user=user,
               speciality=speciality,
               biography=biography,
               location=location,
            )

         elif user.role == "PATIENT":
               Patient.objects.create(
                 user=user
            )    

        return user       


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)     


    def validate(self, data):
        user= authenticate(
            email=data["email"],
            password=data["password"]
        )
        if user is None : 
            raise serializers.ValidationError(
                "invalide email or password"
            )
        data["user"]  = user   
        return data


