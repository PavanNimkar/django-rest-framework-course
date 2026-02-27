from home.views import (
    index,
    person,
    CheckRequest,
    PersonsViewSet,
    RegisterAPI,
    LoginAPI,
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"persons", PersonsViewSet, basename="person")
urlpatterns = router.urls

urlpatterns = [
    path("index", index),
    path("person/", person),
    path("check-request", CheckRequest.as_view()),
    path("router-api/", include(router.urls)),
    path("register/", RegisterAPI.as_view()),
    path("login/", LoginAPI.as_view()),
]
