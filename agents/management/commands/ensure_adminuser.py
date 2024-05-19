import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from agents.management.commands.utils import get_prod_credentials


class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument("--username", help="Admin's username")
        parser.add_argument("--email", help="Admin's email")
        parser.add_argument("--password", help="Admin's password")
        parser.add_argument(
            "--noinput", help="Read options from the environment", action="store_true"
        )
        parser.add_argument(
            "--prod", help="Are you running in production?", action="store_true"
        )

    def handle(self, *args, **options):
        User = get_user_model()
        # get password first
        if options["noinput"]:
            if options["prod"]:
                print("[!] Getting password from AWS Secrets Manager ...")
                prod_credentials = get_prod_credentials()
                options["username"] = prod_credentials["username"]
                options["password"] = prod_credentials["password"]
            else:
                print("[!] Getting password from environment ...")
                options["username"] = os.environ["DJANGO_SUPERUSER_USERNAME"]
                options["password"] = os.environ["DJANGO_SUPERUSER_PASSWORD"]
            options["email"] = os.environ["DJANGO_SUPERUSER_EMAIL"]

        if not User.objects.filter(username=options["username"]).exists():
            print("[!] Creating admin user ...")
            User.objects.create_superuser(
                username=options["username"],
                email=options["email"],
                password=options["password"],
            )

        else:
            print(" [!] Admin user already exists")
