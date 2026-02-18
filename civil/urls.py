from django.urls import path
from .views import analyze_boq

urlpatterns = [
    path('<int:project_id>/analyze-boq/', analyze_boq, name='analyze_boq'),
    # or with trailing slash explicit (Django APPEND_SLASH will handle both):
    # path('<int:project_id>/analyze-boq/', analyze_boq, name='analyze_boq'),
]