from django.urls import path
from .views import analyze_boq

urlpatterns = [
    path('projects/<int:project_id>/analyze-boq/', analyze_boq),
]