from rest_framework import views, status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import boto3
import json
from django.conf import settings


class BucketApi(views.APIView):
    """
    AWS S3 Bucket API for viewing contents of Conductor Buckets
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List contents of a bucket",
        manual_parameters=[
            openapi.Parameter(
                name="bucket_name",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Name of the bucket",
                enum=settings.CONDUCTOR_BUCKETS,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        """
        List contents of a bucket
        """
        bucket_name = request.query_params.get("bucket_name")
        s3 = boto3.client("s3")
        response = s3.list_objects_v2(Bucket=bucket_name)
        return Response(response["Contents"], status=status.HTTP_200_OK)


class BucketObjectApi(views.APIView):
    """
    AWS S3 Bucket Object API for viewing contents of Conductor Buckets
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get contents of a bucket object",
        manual_parameters=[
            openapi.Parameter(
                name="bucket_name",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Name of the bucket",
                enum=settings.CONDUCTOR_BUCKETS,
            ),
            openapi.Parameter(
                name="object_name",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Name of the object",
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        """
        Get contents of a bucket object
        """
        bucket_name = request.query_params.get("bucket_name")
        object_name = request.query_params.get("object_name")
        s3 = boto3.client("s3")
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
        return Response(json.loads(response["Body"].read()), status=status.HTTP_200_OK)


class BucketObjectLatestView(views.APIView):
    """
    Get latest object from a bucket
    Implementing this: https://stackoverflow.com/questions/45375999/how-to-download-the-latest-file-of-an-s3-bucket-using-boto3
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get contents of a bucket object",
        manual_parameters=[
            openapi.Parameter(
                name="bucket_name",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Name of the bucket",
                enum=settings.CONDUCTOR_BUCKETS,
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        """
        Get contents of a bucket object
        """
        bucket_name = request.query_params.get("bucket_name")
        s3 = boto3.client("s3")
        objs = s3.list_objects_v2(Bucket=bucket_name)["Contents"]
        last_added = [
            obj["Key"]
            for obj in sorted(
                objs,
                key=lambda obj: int(obj["LastModified"].strftime("%s")),
                reverse=True,
            )
        ][0]
        response = s3.get_object(Bucket=bucket_name, Key=last_added)
        return Response(json.loads(response["Body"].read()), status=status.HTTP_200_OK)
