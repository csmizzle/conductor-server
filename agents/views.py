"""
Run, create, and manage agents
"""
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from agents import models, serializers
from agents.crews.marketing import market_email_crew


class MarketEmailCrewViewSet(views.APIView):
    """View for taking market crew requests"""

    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        data = models.AgentRun.objects.all().filter(created_by=request.user)
        serialized_runs = serializers.AgentRunSerializer(data, many=True)
        return Response(
            serialized_runs.data,
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=serializers.AgentInput)
    @method_decorator(cache_page(60 * 60 * 2))
    def post(self, request: Request) -> Response:
        """Send a request to the marketing team to email the crew

        Args:
            request (_type_): Request from the client
        """
        agent_input = serializers.AgentInput(data=request.data)
        agent_input.is_valid(raise_exception=True)
        results = market_email_crew.kickoff(
            {"input": agent_input.validated_data["task"]}
        )
        run = models.AgentRun.objects.create(
            task=agent_input.validated_data["task"],
            agent_name="market_email_crew",
            output=results,
        )
        run.save()
        return Response(
            {
                "task": run.task,
                "agent_name": run.agent_name,
                "output": run.output,
            },
            status=status.HTTP_201_CREATED,
        )
