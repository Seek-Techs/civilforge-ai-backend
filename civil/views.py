from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .agents.boq_agent import boq_agent   # this line fails if file missing

@api_view(['GET', 'POST'])
def analyze_boq(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        
        # For GET: just return current saved output (if any)
        if request.method == 'GET':
            if project.boq_output:
                return Response(project.boq_output)
            else:
                return Response({"message": "No BOQ analysis yet. Send POST to trigger."})
        
        # POST: run agent
        result = boq_agent(project.description)
        # Handle if result is dict or BaseModel
        output = result.dict() if hasattr(result, 'dict') else result
        project.boq_output = output
        project.save()
        return Response(output)
    
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)