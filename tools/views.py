from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ToolSerializer
from .models import Tool
from projects.models import Project
from django.shortcuts import get_object_or_404


class ToolListCreateView(APIView):
    permission_classes=[permissions.IsAuthenticated]


    def get(self,request,project_id):
        project=get_object_or_404(Project,id=project_id,owner=request.user)
        tools=Tool.objects.filter(project=project)
        serializer=ToolSerializer(tools,many=True)
        return Response(serializer.data)

    def post(self,request,project_id):
        project=get_object_or_404(Project,id=project_id,owner=request.user)
        serializer=ToolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
class ToolDetailView(APIView):
    permission_classes=[permissions.IsAuthenticated]


    def get_object(self,project_id,pk,user):
        project=get_object_or_404(Project,id=project_id,owner=user)
        return get_object_or_404(Tool,id=pk,project=project)

    def get(self,request,project_id,pk):
        tool=self.get_object(project_id,pk,request.user)
        serializer=ToolSerializer(tool)
        return Response(serializer.data)

    def put(self,request,project_id,pk):
        tool=self.get_object(project_id,pk,request.user)
        serializer=ToolSerializer(tool,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,project_id,pk):
        tool=self.get_object(project_id,pk,request.user)
        tool.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        