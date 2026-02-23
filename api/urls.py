from home.views import index, person, login_view, CheckRequest, PersonsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"persons", PersonsViewSet, basename="person")
urlpatterns = router.urls

urlpatterns = [
    path("index", index),
    path("person/", person),
    path("login", login_view),
    path("check-request", CheckRequest.as_view()),
    path("persons", include(router.urls)),
]
