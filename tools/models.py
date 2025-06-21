from django.db import models
from projects.models import Project

# Create your models here.

Tool_Type_choices=(
    ('code','Code Snippet'),
    ('api','Api Config'),
    ('note','Note'),
    ('env','Environment variables')
)


class Tool(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tools')
    name=models.CharField(max_length=255)
    type=models.CharField(max_length=20,choices=Tool_Type_choices)
    content=models.TextField()
    file=models.FileField(upload_to='tool_files/',blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type})"
    
    

