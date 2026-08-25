import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Crea de forma idempotente el superusuario educativo definido por entorno."

    def handle(self, *args, **options):
        variable_names = (
            "DJANGO_SUPERUSER_USERNAME",
            "DJANGO_SUPERUSER_EMAIL",
            "DJANGO_SUPERUSER_PASSWORD",
        )
        values = {name: os.getenv(name, "").strip() for name in variable_names}

        if not any(values.values()):
            self.stdout.write(
                self.style.WARNING("Superusuario omitido: no se configuraron credenciales.")
            )
            return

        missing = [name for name, value in values.items() if not value]
        if missing:
            raise CommandError(
                "Faltan variables para crear el superusuario: " + ", ".join(missing)
            )

        user_model = get_user_model()
        username = values["DJANGO_SUPERUSER_USERNAME"]
        if user_model.objects.filter(username=username).exists():
            self.stdout.write(f"El superusuario '{username}' ya existe; no se modificó.")
            return

        user_model.objects.create_superuser(
            username=username,
            email=values["DJANGO_SUPERUSER_EMAIL"],
            password=values["DJANGO_SUPERUSER_PASSWORD"],
        )
        self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' creado."))
