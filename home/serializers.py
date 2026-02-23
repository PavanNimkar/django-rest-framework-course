from rest_framework import serializers
from .models import Person, Role


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["role_name"]


class PersonSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    company = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = "__all__"

    def get_company(self, obj):
        person_name = obj.name
        person_role = Role.objects.get(id=obj.role.id)

        return f"{person_name} ({person_role}) at Meta"

    def validate(self, data):
        if data["age"] < 18:
            raise serializers.ValidationError("age must be greater than 18")

        special_char = "!@#$%^&*()_+~`_"
        if any(c in special_char for c in data["name"]):
            raise serializers.ValidationError("Name must not contain sepcial chracters")
        return data
