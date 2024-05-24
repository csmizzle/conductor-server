from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from chains import serializers
from chains import models
from chains.tasks import run_summary_task
from conductor import chains
from conductor.functions import apollo
import json


class ReadCreateModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    """Task view set"""

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChainTaskSerializer
    queryset = models.ChainTask.objects.all()
    lookup_field = "task_id"
    lookup_url_kwarg = "task_id"


class SummarizeContentViewSet(ReadCreateModelViewSet):
    """
    API endpoint that allows summaries to be created and retrieved.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChainSummarySerializer
    queryset = models.Summary.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=serializers.CreateChainSummarizeContentSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new summary.
        """
        request_serializer = serializers.CreateChainSummarizeContentSerializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)
        task = models.ChainTask.objects.create(created_by=request.user)
        run_summary_task.delay(
            task_id=task.task_id, content=request_serializer.validated_data["content"]
        )
        task_serializer = serializers.ChainTaskSerializer(task)
        return Response(task_serializer.data, status=status.HTTP_201_CREATED)


class ApolloInputChainView(ReadCreateModelViewSet):
    """
    API endpoint that allows for Apollo inputs to be created
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChainEventSerializer
    queryset = models.ChainEvent.objects.all().filter(
        chain_name=chains.create_apollo_input_structured.__name__
    )
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=serializers.CreateApolloInputSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new Apollo input
        """
        request_serializer = serializers.CreateApolloInputSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        apollo_input = chains.create_apollo_input_structured(
            query=request_serializer.validated_data["query"]
        )
        response_serializer = serializers.ChainEventSerializer(
            data={
                "created_by": request.user.id,
                "chain_name": chains.create_apollo_input_structured.__name__,
                "input": request_serializer.validated_data["query"],
                "output": apollo_input.dict(),
            }
        )
        response_serializer.is_valid(raise_exception=True)
        response_serializer.save()
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ApolloContextChainView(ReadCreateModelViewSet):
    """
    API endpoint that allows for Apollo context to be created
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChainEventSerializer
    queryset = models.ChainEvent.objects.all().filter(
        chain_name=apollo.generate_apollo_person_search_context.__name__
    )
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=serializers.ApolloContextInputChain,
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new Apollo context
        """
        request_serializer = serializers.ApolloContextInputChain(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        apollo_context = apollo.generate_apollo_person_search_context(
            person_titles=request_serializer.validated_data["person_titles"],
            person_locations=request_serializer.validated_data["person_locations"],
        )
        response_serializer = serializers.ChainEventSerializer(
            data={
                "created_by": request.user.id,
                "chain_name": apollo.generate_apollo_person_search_context.__name__,
                "input": json.dumps(
                    {
                        "person_titles": request_serializer.validated_data[
                            "person_titles"
                        ],
                        "person_locations": request_serializer.validated_data[
                            "person_locations"
                        ],
                    }
                ),
                "output": apollo_context,
            }
        )
        response_serializer.is_valid(raise_exception=True)
        response_serializer.save()
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CreateEmailChainView(ReadCreateModelViewSet):
    """
    API endpoint that allows for Apollo context to be created
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChainEventSerializer
    queryset = models.ChainEvent.objects.all().filter(
        chain_name=chains.create_email_from_context_structured.__name__
    )
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=serializers.EmailFromContextSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new Apollo context
        """
        request_serializer = serializers.EmailFromContextSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        email_from_context = chains.create_email_from_context(
            tone=request_serializer.validated_data["tone"],
            context=request_serializer.validated_data["context"],
            sign_off=request_serializer.validated_data["sign_off"],
        )
        response_serializer = serializers.ChainEventSerializer(
            data={
                "created_by": request.user.id,
                "chain_name": chains.create_email_from_context_structured.__name__,
                "input": json.dumps(
                    {
                        "tone": request_serializer.validated_data["tone"],
                        "context": request_serializer.validated_data["context"],
                        "sign_off": request_serializer.validated_data["sign_off"],
                    }
                ),
                "output": email_from_context,
            }
        )
        response_serializer.is_valid(raise_exception=True)
        response_serializer.save()
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
