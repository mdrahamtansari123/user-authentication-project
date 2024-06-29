from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register("standard", views.StandardViewSet, basename="standard")
router.register("subject", views.SubjectViewSet, basename="subject")

urlpatterns = [
    path('', include(router.urls)),
   
   
    
]