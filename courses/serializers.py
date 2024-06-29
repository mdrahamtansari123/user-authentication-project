from rest_framework import request, serializers
# from user.models import Person
from . import models





class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Standard
        fields = ["id", "standard_name", "image","created_at", "created_by"]

    def validate(self, data):
        if "created_by" in self.context:
            data["created_by"] = self.context[
                "created_by"
            ] 
        return data
    
class SubjectSerializer(serializers.ModelSerializer):
    standard_name = serializers.SerializerMethodField(
        "get_standard_name", read_only=True
    )

    class Meta:
        model = models.Subject
        fields = [
            "id",
            "standard_id",
            "subject_name",
            "subject_image",
            "created_at",
            "standard_name",
            "created_by",
        ]
        extra_kwargs = {"standard_id": {"write_only": True}}

        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('standard_id', 'subject_name'),
                message="subject already exists"
            )
        ]

    def validate(self, data):
        if "created_by" in self.context:
            data["created_by"] = self.context["created_by"]
        return data


    def get_standard_name(self, obj):
        return obj.standard_id.standard_name