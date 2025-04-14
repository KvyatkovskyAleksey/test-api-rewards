from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import os


class Command(BaseCommand):
    ADMIN_USER = os.environ.get("ADMIN_USER", "admin@admin.com")
    ADMIN_PASS = os.environ.get("ADMIN_PASS", "12345")

    def __init__(self):
        self.user = get_user_model()
        super(Command, self).__init__()

    def add_arguments(self, parser):
        parser.add_argument(
            "--create-superuser",
            action="store_true",
            default=False,
            help="password of the admin user",
        )
        parser.add_argument(
            "--admin-user", default=self.ADMIN_USER, help="the admin user to create"
        )
        parser.add_argument(
            "--admin-pass", default=self.ADMIN_PASS, help="password of the admin user"
        )
        parser.add_argument("--run_cfb_api_spiders", help="Run cfb API spiders")

    def success(self, text):
        self.stdout.write(self.style.SUCCESS(text))

    def todo(self, text):
        self.stdout.write(self.style.NOTICE(text))

    def skip(self, text):
        self.stdout.write(self.style.WARNING(text))

    def handle(self, *args, **options):

        if options.get("create_superuser"):
            username = options["admin_user"]
            password = options["admin_pass"]

            if not self._is_admin_user_exists(username):

                self._create_admin_user(username, password)
                self.success("Created the admin user.")

            else:
                self.skip("Skipped to create admin user, already exists.")

            self.success(
                f"Admin user is ready, you can login "
                f"with username {username} and password {password} now."
            )

        if options.get("run_cfb_api_spiders"):
            logger.info("need to set command")

        self.success("Data population succeed.")

    def _is_admin_user_exists(self, username):
        return self.user.objects.filter(username=username).exists()

    def _create_admin_user(self, username, password):
        self.user.objects.create_superuser(
            username=username, email=username, password=password
        )
