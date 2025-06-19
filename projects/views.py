from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions
from .models import Project
from .serializers import ProjectSerializer
from django.shortcuts import get_object_or_404
from .permissions import Isowner

class ProjectListCreateView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        projects=Project.objects.filter(owner=request.user)
        serializer=ProjectSerializer(projects,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ProjectDetailView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self,pk,user):
        return get_object_or_404(Project,pk=pk,owner=user)
    
    def get(self,request,pk):
        project=self.get_object(pk,request.user)
        serializer=ProjectSerializer(project)
        return Response(serializer.data)
    
    def put(self,request,pk):
        project=self.get_object(pk,request.user)
        serializer=ProjectSerializer(project,data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        project=self.get_object(pk,request.user)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
