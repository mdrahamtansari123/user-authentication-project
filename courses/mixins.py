from rest_framework import status, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class CourseMixin(viewsets.ModelViewSet):
    create_response = {"status": "success", "message": "course created"}
    get_response = {"status": "success", "message": ""}
    update_response = {"status": "success", "message": "course updated"}
    delete_response = {"status": "success", "message": "course deleted"}

    def create(self, request, *args, **kwargs):
        context = {"created_by": request.user.id}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.create_response["data"] = serializer.data
        return Response(self.create_response, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(obj)
        self.get_response["data"] = serializer.data
        return Response(self.get_response, status=status.HTTP_200_OK)

    def partial_update(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        self.delete_media_files(obj)  # Make sure to define this method if needed
        serializer = self.get_serializer(data=request.data, instance=obj, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.update_response["data"] = serializer.data
        return Response(self.update_response, status=status.HTTP_200_OK)

    def destroy(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        self.perform_destroy(obj)
        return Response(self.delete_response, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        self.delete_media_files(instance)  # Implement this method if needed
        instance.delete()