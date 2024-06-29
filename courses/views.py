from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from . import models, serializers
from rest_framework import parsers
from .mixins import CourseMixin
from rest_framework.permissions import IsAuthenticated


class StandardViewSet(CourseMixin):
    filter_fields = ["standard_name"]
    ordering = ["created_at"]
    # authentication_classes = [IsAuthOrReadOnly]
    queryset = models.Standard.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    serializer_class = serializers.StandardSerializer
    model = models.Standard
    delete_response = {"status": "success", "message": "standard deleted"}
    update_response = {"status": "success", "message": "standard updated"}
    get_response = {"status": "success", "message": ""}
    create_response = {"status": "success", "message": "standard created"}


class SubjectViewSet(CourseMixin):
    filter_fields = ["standard_id__standard_name","subject_name"]
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]

    # permission_classes = [IsAdminUser,IsSuperUser,IsRegularUser]
    # permission_classes = [IsAdminOrReadOnly] 
    queryset = models.Subject.objects.all()
    ordering = ["created_at"]
    serializer_class = serializers.SubjectSerializer
    model = models.Subject
    delete_response = {"status": "success", "message": "subject deleted"}
    update_response = {"status": "success", "message": "subject updated"}
    get_response = {"status": "success", "message": ""}
    create_response = {"status": "success", "message": "subject created"}