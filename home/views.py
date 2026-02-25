from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PersonSerializer, LoginSerializer, RegistrationSerializer
from rest_framework import viewsets
from .models import Person
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# Create your views here.
@api_view(["GET"])
def index(request):
    courses = {
        "languages": ["python", "javascript"],
        "duration": "3 months",
        "price": 100,
    }

    return Response(courses)


class CheckRequest(APIView):
    def get(self, request):
        return Response({"message": f"this is a {request.method} request"})

    def post(self, request):
        return Response({"message": f"this is a {request.method} request"})

    def put(self, request):
        return Response({"message": f"this is a {request.method} request"})

    def patch(self, request):
        return Response({"message": f"this is a {request.method} request"})

    def delete(self, request):
        return Response({"message": f"this is a {request.method} request"})


@api_view(["GET", "POST", "PATCH", "PUT", "DELETE"])
def person(request):
    if request.method == "GET":
        # query set data from database
        objs = Person.objects.filter(role__isnull=False)
        # coverting this into JSON
        serializer = PersonSerializer(objs, many=True)

        return Response(serializer.data)

    elif request.method == "POST":
        # JSON data from frontend
        data = request.data
        # converting into queryset
        serializer = PersonSerializer(data=data)
        # validating data fields
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "PUT":
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "PATCH":
        data = request.data
        obj = Person.objects.get(id=data["id"])
        serializer = PersonSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    else:
        data = request.data
        obj = Person.objects.get(id=data["id"])
        obj.delete()
        return Response({"message": "Object deleted"})


class PersonsViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def list(self, request):
        search = request.GET.get("search")
        queryset = self.queryset
        if search:
            queryset = queryset.filter(name__startswith=search)
            serializer = PersonSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response(
            {"message": "user created!"},
            status=status.HTTP_201_CREATED,
        )


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                {"message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            username=serializer.data["username"], password=serializer.data["password"]
        )

        if not user:
            return Response(
                {"message": "User not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        return Response(
            {"message": "user logged in!", "token": f"{token}"},
            status=status.HTTP_200_OK,
        )
