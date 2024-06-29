from django.db import models
from uuid import uuid4



class CommonFields(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,unique=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        abstract = True

    def __str__(self) -> str:
        return str(self.id)
    
class Standard(CommonFields):
    standard_name = models.CharField(max_length=100, unique=True)
    image = models.FileField(upload_to="image/standard")

    class Meta:
        db_table = "standard"

    def __str__(self):
        return f"{self.standard_name}"
    

class Subject(CommonFields):
    standard_id = models.ForeignKey(
        Standard,
        on_delete=models.CASCADE,
        related_name="standard_subjects",
        db_column="standard_id",
    )
    subject_name = models.CharField(max_length=50)
    subject_image = models.FileField(upload_to='image/subject')
    class Meta:
        db_table = "subject"

    def __str__(self):
        return f"{self.subject_name} [ + {self.standard.standard_name} ]"