from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *


@api_view(["GET", "POST"])
def index(request):

    courses = {
        "course": "Python",
        "Frameworks": ["Flask", "FastAPI", "Django", "Django Rest Framework"],
        "provider": "Abhijeet Gupta",
    }

    if request.method == "GET":
        data = request.GET.get("search")
        print(data)

    if request.method == "POST":
        data = request.data
        print(data)

    return Response(courses)


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE"])
def person(request):
    if request.method == "GET":
        objs = Person.objects.all()
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == "PUT":
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == "PATCH":
        data = request.data
        objs = Person.objects.get(id=data["id"])
        serializer = PeopleSerializer(objs, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    else:
        data = request.data
        objs = Person.objects.get(id=data["id"])
        objs.delete()
        return Response({"message": "Person Deleted"})
