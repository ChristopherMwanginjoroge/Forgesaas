from django.urls import path
from .views import ToolListCreateView, ToolDetailView

urlpatterns = [
    path('<int:project_id>/tools/', ToolListCreateView.as_view(), name='tool-list-create'),
    path('<int:project_id>/tools/<int:pk>/', ToolDetailView.as_view(), name='tool-detail'),
]
