from conductor.functions.pinecone_ import search_pinecone
from conductor.retrievers.pinecone_ import (
    create_gpt4_pinecone_apollo_retriever,
    create_gpt4_pinecone_discord_retriever,
)
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from search.serializers import SearchInputSerializer

apollo_search = create_gpt4_pinecone_apollo_retriever()
discord_search = create_gpt4_pinecone_discord_retriever()


class ApolloSearchView(views.APIView):
    """Search view for Apollo data"""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SearchInputSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        """Get Apollo search results"""
        input_serializer = SearchInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        results = apollo_search(input_serializer.data["query"])
        return Response(results, status=status.HTTP_200_OK)


class DiscordSearchView(views.APIView):
    """Search view for Discord data"""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SearchInputSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        """Get Discord search results"""
        input_serializer = SearchInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        results = apollo_search(input_serializer.data["query"])
        return Response(results, status=status.HTTP_200_OK)


class PineconeSearchView(views.APIView):
    """Search view for Pinecone data"""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SearchInputSerializer)
    def post(self, request: Request, *args, **kwargs) -> Response:
        """Get Pinecone search results"""
        input_serializer = SearchInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        results = search_pinecone(input_serializer.data["query"])
        return Response(results, status=status.HTTP_200_OK)
