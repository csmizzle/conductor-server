from typing import Union
from django.conf import settings
import boto3
import json


def get_prod_credentials() -> Union[dict, None]:
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=settings.AWS_DEFAULT_REGION,
    )
    get_secret_value_response = client.get_secret_value(
        SecretId=settings.AWS_PROD_SECRET_NAME
    )
    if "SecretString" in get_secret_value_response:
        secret = get_secret_value_response["SecretString"]
        return json.loads(secret)
