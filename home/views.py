from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PersonSerializer
from .models import Person


# Create your views here.
@api_view(["GET"])
def index(request):
    courses = {
        "languages": ["python", "javascript"],
        "duration": "3 months",
        "price": 100,
    }

    return Response(courses)


@api_view(["GET", "POST", "PATCH", "PUT", "DELETE"])
def person(request):
    if request.method == "GET":
        # query set data from database
        objs = Person.objects.all()
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
