from rest_framework import serializers
from .models import Person
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data["username"]:
            if User.objects.filter(username=data["username"]).exists():
                raise serializers.ValidationError("User already exists!")
        if data["email"]:
            if User.objects.filter(email=data["email"]).exists():
                raise serializers.ValidationError("Email already exists!")

        return data

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = "__all__"

    def validate(self, data):
        if data["age"] < 18:
            raise serializers.ValidationError("age must be greater than 18")

        special_char = "!@#$%^&*()_+~`_"
        if any(c in special_char for c in data["name"]):
            raise serializers.ValidationError("Name must not contain sepcial chracters")
        return data
