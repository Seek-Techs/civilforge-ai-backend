from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from .agents.boq_agent import boq_agent

@api_view(['POST'])
def analyze_boq(request, project_id):
    project = Project.objects.get(id=project_id)
    result = boq_agent(project.description)
    project.boq_output = result.dict()
    project.save()
    return Response(result.dict())