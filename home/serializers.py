from rest_framework import serializers
from .models import Person


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
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
