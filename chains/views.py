import json
from conductor import chains
from conductor.functions import apollo
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chains import models, serializers
from flows import models as flow_models
from chains.tasks import run_summary_task


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
    lookup_field = "task_id"
    lookup_url_kwarg = "task_id"

    def get_queryset(self):
        return models.ChainTask.objects.filter(created_by=self.request.user)


class SummarizeContentViewSet(ReadCreateModelViewSet):
    """
    API endpoint that allows summaries to be created and retrieved.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChainSummarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Summary.objects.filter(created_by=self.request.user)

    @swagger_auto_schema(
        request_body=serializers.CreateChainSummarizeContentSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new summary.
        """
        flow_trace = None
        request_serializer = serializers.CreateChainSummarizeContentSerializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)
        if request_serializer.validated_data.get("flow_trace"):
            flow_trace = flow_models.FlowTrace.objects.get(
                id=request_serializer.validated_data.get("flow_trace"),
                created_by=request.user,
            )
        event = models.ChainEvent.objects.create(
            flow_trace=flow_trace,
            created_by=request.user,
            chain_name=chains.map_reduce_summarize.__name__,
            input=json.dumps(request_serializer.validated_data),
        )
        task = models.ChainTask.objects.create(created_by=request.user)
        run_summary_task.delay(
            event_id=event.id,
            task_id=task.task_id,
            content=request_serializer.validated_data["content"],
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
        chain_name=chains.create_apollo_input_structured.__name__,
    )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    @swagger_auto_schema(
        request_body=serializers.CreateApolloInputSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new Apollo input
        """
        flow_trace = None
        request_serializer = serializers.CreateApolloInputSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        if request_serializer.validated_data.get("flow_trace"):
            flow_trace = flow_models.FlowTrace.objects.get(
                id=request_serializer.validated_data.get("flow_trace"),
                created_by=request.user,
            )
        apollo_input = chains.create_apollo_input_structured(
            query=request_serializer.validated_data["query"]
        )
        response_serializer = serializers.ChainEventSerializer(
            data={
                "flow_trace": flow_trace.id if flow_trace else None,
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

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    @swagger_auto_schema(
        request_body=serializers.ApolloContextInputChain,
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new Apollo context
        """
        flow_trace = None
        request_serializer = serializers.ApolloContextInputChain(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        if request_serializer.validated_data.get("flow_trace"):
            flow_trace = flow_models.FlowTrace.objects.get(
                id=request_serializer.validated_data.get("flow_trace"),
                created_by=request.user,
            )
        apollo_context = apollo.generate_apollo_person_search_context(
            person_titles=request_serializer.validated_data["person_titles"],
            person_locations=request_serializer.validated_data["person_locations"],
        )
        response_serializer = serializers.ChainEventSerializer(
            data={
                "flow_trace": flow_trace.id if flow_trace else None,
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

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    @swagger_auto_schema(
        request_body=serializers.EmailFromContextSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new Apollo context
        """
        flow_trace = None
        request_serializer = serializers.EmailFromContextSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        if request_serializer.validated_data.get("flow_trace"):
            flow_trace = flow_models.FlowTrace.objects.get(
                id=request_serializer.validated_data.get("flow_trace"),
                created_by=request.user,
            )
        email_from_context = chains.create_email_from_context(
            tone=request_serializer.validated_data["tone"],
            context=request_serializer.validated_data["context"],
            sign_off=request_serializer.validated_data["sign_off"],
        )
        response_serializer = serializers.ChainEventSerializer(
            data={
                "flow_trace": flow_trace.id if flow_trace else None,
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


class ApolloUrlContextChainView(ReadCreateModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChainEventSerializer
    queryset = models.ChainEvent.objects.all().filter(
        chain_name=apollo.generate_apollo_person_domain_search_context.__name__
    )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)

    @swagger_auto_schema(
        request_body=serializers.ApolloUrlContextInputChain,
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new Apollo context
        """
        flow_trace = None
        request_serializer = serializers.ApolloUrlContextInputChain(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        if request_serializer.validated_data.get("flow_trace"):
            flow_trace = flow_models.FlowTrace.objects.get(
                id=request_serializer.validated_data.get("flow_trace"),
                created_by=request.user,
            )
        apollo_context = apollo.generate_apollo_person_domain_search_context(
            company_domains=request_serializer.validated_data["company_domains"],
        )
        response_serializer = serializers.ChainEventSerializer(
            data={
                "flow_trace": flow_trace.id if flow_trace else None,
                "created_by": request.user.id,
                "chain_name": apollo.generate_apollo_person_domain_search_context.__name__,
                "input": json.dumps(
                    {
                        "company_domains": request_serializer.validated_data[
                            "company_domains"
                        ]
                    }
                ),
                "output": apollo_context,
            }
        )
        response_serializer.is_valid(raise_exception=True)
        response_serializer.save()
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
