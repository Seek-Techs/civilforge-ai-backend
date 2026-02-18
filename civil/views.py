# civil/views.py
import logging
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Project
from langchain_core.messages import HumanMessage
from .agents.boq_graph import graph  # adjust path if needed

logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def analyze_boq(request, project_id):
    try:
        project = Project.objects.select_related('owner').get(id=project_id)

        # Ownership check
        if project.owner != request.user:
            return Response(
                {"detail": "You do not have permission to analyze this project."},
                status=status.HTTP_403_FORBIDDEN
            )

        if request.method == 'GET':
            if project.boq_output:
                return Response(project.boq_output)
            return Response({
                "message": "No BOQ analysis available yet. Send POST to start."
            })

        # POST ──────────────────────────────────────────────────────
        if not project.description or not project.description.strip():
            return Response(
                {"detail": "Project description is required for BOQ generation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            initial_state = {
                "description": project.description,
                "messages": [HumanMessage(content=project.description)],
                "boq_result": None
            }

            try:
                final_state = graph.invoke(
                    initial_state,
                    {"recursion_limit": 60, "max_iterations": 30}  # safety caps
                )
                output = final_state.get("boq_result")

                if output is None:
                    raise ValueError("Agent returned no valid BOQ result")

                project.boq_output = output
                project.save(update_fields=['boq_output'])

                logger.info(f"BOQ generated for project {project_id} by user {request.user.id}")
                return Response(output)

            except Exception as agent_exc:
                logger.exception(f"Agent failed for project {project_id}: {str(agent_exc)}")
                return Response(
                    {
                        "detail": "BOQ generation failed. Please try again or contact support.",
                        "error_type": agent_exc.__class__.__name__,
                        # "trace": str(final_state)  # optional — careful with size
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    except Project.DoesNotExist:
        return Response({"detail": "Project not found"}, status=404)
    except ValidationError as ve:
        return Response({"detail": str(ve)}, status=400)
    except Exception as e:
        logger.exception(f"Unexpected error in analyze_boq: {str(e)}")
        return Response({"detail": "Internal server error"}, status=500)