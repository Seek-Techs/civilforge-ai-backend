# civil/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Project

# Import what you actually use
from langchain_core.messages import HumanMessage
from .agents.boq_graph import graph   # ← assuming you named the file boq_graph.py


@api_view(['GET', 'POST'])
def analyze_boq(request, project_id):
    try:
        project = Project.objects.get(id=project_id)

        if request.method == 'GET':
            if project.boq_output:
                return Response(project.boq_output)
            return Response({
                "message": "No BOQ analysis yet. Send a POST request to trigger analysis."
            })

        # ── POST ───────────────────────────────────────────────
        if not project.description.strip():
            return Response(
                {"error": "Project description is empty. Cannot generate BOQ."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            initial_state = {
                "description": project.description,
                "messages": [HumanMessage(content=project.description)],
                "boq_result": None
            }

            try:
                final_state = graph.invoke(initial_state, {"recursion_limit": 50})
                output = final_state.get("boq_result")

                if output is None:
                    raise ValueError("Agent did not produce a valid BOQ result")

                project.boq_output = output
                project.save(update_fields=["boq_output"])

                return Response(output)

            except Exception as agent_error:
                # You can log this properly later (structlog, sentry, etc.)
                return Response(
                    {
                        "error": "Agent execution failed",
                        "detail": str(agent_error)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)