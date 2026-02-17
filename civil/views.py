from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .agents.boq_agent import boq_agent   # this line fails if file missing

@api_view(['POST'])
def analyze_boq(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        result = boq_agent(project.description)
        project.boq_output = result.dict() if hasattr(result, 'dict') else result
        project.save()
        return Response(result.dict() if hasattr(result, 'dict') else result, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)