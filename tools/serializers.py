from rest_framework import serializers
from .models import Tool

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tool
        fields = ['id', 'project', 'name', 'type','file', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']